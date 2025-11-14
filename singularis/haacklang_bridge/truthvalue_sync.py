"""
TruthValue Synchronization Protocol

Handles bidirectional synchronization of truthvalues between
Python subsystems and HaackLang runtime.
"""

from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass, field
import time
from collections import defaultdict


@dataclass
class TruthValueUpdate:
    """Represents a truthvalue update event."""
    name: str
    track: str
    old_value: float
    new_value: float
    timestamp: float
    source: str  # 'python' or 'haacklang'
    
    def delta(self) -> float:
        """Get the change in value."""
        return self.new_value - self.old_value


@dataclass
class SyncStats:
    """Statistics for truthvalue synchronization."""
    total_updates: int = 0
    python_to_haack: int = 0
    haack_to_python: int = 0
    conflicts: int = 0
    avg_latency_ms: float = 0.0
    update_rate_hz: float = 0.0


class TruthValueSync:
    """
    Manages bidirectional synchronization of truthvalues.
    
    Features:
    - Automatic propagation Python ↔ HaackLang
    - Conflict detection and resolution
    - Change notification callbacks
    - Synchronization statistics
    """
    
    def __init__(self, runtime):
        """
        Initialize sync protocol.
        
        Args:
            runtime: HaackLangRuntime instance
        """
        self.runtime = runtime
        
        # Track current values
        self.current_values: Dict[str, Dict[str, float]] = defaultdict(dict)
        
        # Update history
        self.update_history: List[TruthValueUpdate] = []
        self.max_history = 1000
        
        # Callbacks for value changes
        self.on_change_callbacks: Dict[str, List[Callable]] = defaultdict(list)
        
        # Statistics
        self.stats = SyncStats()
        self.start_time = time.time()
        
        # Conflict resolution strategy
        self.conflict_strategy = 'trust_newer'  # or 'trust_python', 'trust_haacklang', 'average'
        
        print("[SYNC] TruthValue synchronization protocol initialized")
    
    def update_from_python(
        self,
        name: str,
        track: str,
        value: float,
        notify_callbacks: bool = True
    ):
        """
        Update a truthvalue from Python side.
        
        Args:
            name: TruthValue name
            track: Track name
            value: New value (0.0-1.0)
            notify_callbacks: Whether to trigger callbacks
        """
        # Get old value
        old_value = self.current_values[name].get(track, 0.0)
        
        # Check for conflict with HaackLang
        haack_value = self.runtime.get_truthvalue(name, track)
        if haack_value is not None and abs(haack_value - value) > 0.1:
            self._resolve_conflict(name, track, value, haack_value, 'python')
            self.stats.conflicts += 1
        
        # Update current values
        self.current_values[name][track] = value
        
        # Propagate to HaackLang
        self.runtime.set_truthvalue(name, track, value)
        
        # Record update
        update = TruthValueUpdate(
            name=name,
            track=track,
            old_value=old_value,
            new_value=value,
            timestamp=time.time(),
            source='python'
        )
        self.update_history.append(update)
        
        # Limit history
        if len(self.update_history) > self.max_history:
            self.update_history.pop(0)
        
        # Update stats
        self.stats.total_updates += 1
        self.stats.python_to_haack += 1
        self._update_stats()
        
        # Notify callbacks
        if notify_callbacks:
            self._notify_callbacks(name, track, old_value, value)
    
    def update_from_haacklang(
        self,
        name: str,
        track: str,
        value: float
    ):
        """
        Update a truthvalue from HaackLang side.
        
        Args:
            name: TruthValue name
            track: Track name
            value: New value
        """
        # Get old value
        old_value = self.current_values[name].get(track, 0.0)
        
        # Update current values
        self.current_values[name][track] = value
        
        # Record update
        update = TruthValueUpdate(
            name=name,
            track=track,
            old_value=old_value,
            new_value=value,
            timestamp=time.time(),
            source='haacklang'
        )
        self.update_history.append(update)
        
        if len(self.update_history) > self.max_history:
            self.update_history.pop(0)
        
        # Update stats
        self.stats.total_updates += 1
        self.stats.haack_to_python += 1
        self._update_stats()
        
        # Notify callbacks
        self._notify_callbacks(name, track, old_value, value)
    
    def register_callback(self, truthvalue_name: str, callback: Callable):
        """
        Register a callback for when a truthvalue changes.
        
        Args:
            truthvalue_name: Name of truthvalue to watch
            callback: Function(name, track, old_value, new_value) to call
        """
        self.on_change_callbacks[truthvalue_name].append(callback)
    
    def _notify_callbacks(self, name: str, track: str, old_value: float, new_value: float):
        """Notify registered callbacks of a change."""
        if name in self.on_change_callbacks:
            for callback in self.on_change_callbacks[name]:
                try:
                    callback(name, track, old_value, new_value)
                except Exception as e:
                    print(f"[SYNC] Callback error for {name}.{track}: {e}")
    
    def _resolve_conflict(
        self,
        name: str,
        track: str,
        python_value: float,
        haack_value: float,
        source: str
    ):
        """
        Resolve conflict between Python and HaackLang values.
        
        Args:
            name: TruthValue name
            track: Track name
            python_value: Value from Python
            haack_value: Value from HaackLang
            source: Which side initiated the update
        """
        print(f"[SYNC] Conflict detected: {name}.{track}")
        print(f"[SYNC]   Python: {python_value:.3f}")
        print(f"[SYNC]   HaackLang: {haack_value:.3f}")
        
        resolved_value = None
        
        if self.conflict_strategy == 'trust_python':
            resolved_value = python_value
            print(f"[SYNC]   Resolution: trust Python → {resolved_value:.3f}")
        
        elif self.conflict_strategy == 'trust_haacklang':
            resolved_value = haack_value
            print(f"[SYNC]   Resolution: trust HaackLang → {resolved_value:.3f}")
        
        elif self.conflict_strategy == 'trust_newer':
            # Trust whichever side just updated
            resolved_value = python_value if source == 'python' else haack_value
            print(f"[SYNC]   Resolution: trust newer ({source}) → {resolved_value:.3f}")
        
        elif self.conflict_strategy == 'average':
            resolved_value = (python_value + haack_value) / 2.0
            print(f"[SYNC]   Resolution: average → {resolved_value:.3f}")
        
        # Apply resolution
        if resolved_value is not None:
            self.current_values[name][track] = resolved_value
            self.runtime.set_truthvalue(name, track, resolved_value)
    
    def get_current_value(self, name: str, track: Optional[str] = None) -> Any:
        """
        Get current synchronized value.
        
        Args:
            name: TruthValue name
            track: Specific track (None = all tracks)
        
        Returns:
            Value or dict of values
        """
        if name not in self.current_values:
            return None
        
        if track:
            return self.current_values[name].get(track, 0.0)
        else:
            return dict(self.current_values[name])
    
    def get_update_history(
        self,
        name: Optional[str] = None,
        track: Optional[str] = None,
        limit: int = 100
    ) -> List[TruthValueUpdate]:
        """
        Get update history.
        
        Args:
            name: Filter by truthvalue name
            track: Filter by track name
            limit: Max number of updates to return
        
        Returns:
            List of updates
        """
        history = self.update_history
        
        if name:
            history = [u for u in history if u.name == name]
        
        if track:
            history = [u for u in history if u.track == track]
        
        return history[-limit:]
    
    def _update_stats(self):
        """Update synchronization statistics."""
        uptime = time.time() - self.start_time
        
        if uptime > 0:
            self.stats.update_rate_hz = self.stats.total_updates / uptime
        
        # Calculate average latency (Python → HaackLang roundtrip)
        if self.update_history:
            recent = self.update_history[-100:]
            latencies = []
            
            for i in range(1, len(recent)):
                if recent[i].source != recent[i-1].source:
                    # Cross-boundary update
                    latency = (recent[i].timestamp - recent[i-1].timestamp) * 1000
                    latencies.append(latency)
            
            if latencies:
                self.stats.avg_latency_ms = sum(latencies) / len(latencies)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get synchronization statistics."""
        return {
            'total_updates': self.stats.total_updates,
            'python_to_haack': self.stats.python_to_haack,
            'haack_to_python': self.stats.haack_to_python,
            'conflicts': self.stats.conflicts,
            'update_rate_hz': self.stats.update_rate_hz,
            'avg_latency_ms': self.stats.avg_latency_ms,
            'tracked_truthvalues': len(self.current_values),
            'conflict_strategy': self.conflict_strategy
        }
    
    def print_status(self):
        """Print sync status."""
        print("\n" + "="*70)
        print("TruthValue Synchronization Status")
        print("="*70)
        
        stats = self.get_stats()
        
        print(f"\nUpdates:")
        print(f"  Total: {stats['total_updates']}")
        print(f"  Python → HaackLang: {stats['python_to_haack']}")
        print(f"  HaackLang → Python: {stats['haack_to_python']}")
        print(f"  Update Rate: {stats['update_rate_hz']:.2f} Hz")
        
        print(f"\nConflicts:")
        print(f"  Total: {stats['conflicts']}")
        print(f"  Strategy: {stats['conflict_strategy']}")
        
        print(f"\nPerformance:")
        print(f"  Avg Latency: {stats['avg_latency_ms']:.2f} ms")
        
        print(f"\nTruthValues:")
        print(f"  Tracked: {stats['tracked_truthvalues']}")
        
        if self.current_values:
            print(f"\nCurrent Values:")
            for name, tracks in list(self.current_values.items())[:10]:
                print(f"  {name}:")
                for track, value in tracks.items():
                    print(f"    {track}: {value:.3f}")
        
        print("="*70 + "\n")
