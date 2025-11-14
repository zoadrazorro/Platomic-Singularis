"""
Singularis↔HaackLang Integration Bridge.

This is the main integration layer that connects Singularis AGI
to HaackLang cognitive modules.
"""

import asyncio
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass

from .runtime import HaackLangRuntime, ExecutionResult
from .decorators import bind_runtime, get_registry


@dataclass
class GameStateMapping:
    """Maps game state to HaackLang context."""
    in_combat: bool = False
    in_menu: bool = False
    in_dialogue: bool = False
    in_exploration: bool = True
    
    def get_context(self) -> str:
        """Determine which HaackLang context to use."""
        if self.in_combat:
            return 'combat'
        elif self.in_menu:
            return 'menu'
        elif self.in_dialogue:
            return 'dialogue'
        else:
            return 'exploration'


class SingularisHaackBridge:
    """
    Main integration bridge between Singularis and HaackLang.
    
    Responsibilities:
    - Manage HaackLang runtime lifecycle
    - Synchronize game state → HaackLang contexts
    - Coordinate beat timing with Singularis main loop
    - Route subsystem outputs → HaackLang truthvalues
    - Execute .haack modules and return decisions
    """
    
    def __init__(
        self,
        haack_modules_dir: Path,
        beat_interval: float = 0.1
    ):
        """
        Initialize the bridge.
        
        Args:
            haack_modules_dir: Directory containing .haack files
            beat_interval: Seconds per beat (default: 0.1s = 10Hz)
        """
        self.haack_modules_dir = Path(haack_modules_dir)
        self.beat_interval = beat_interval
        
        # Initialize HaackLang runtime
        self.runtime = HaackLangRuntime(beat_interval=beat_interval)
        
        # Bind runtime to decorators
        bind_runtime(self.runtime)
        
        # Game state
        self.game_state = GameStateMapping()
        
        # Loaded modules
        self.loaded_modules: List[str] = []
        
        # Statistics
        self.stats = {
            'total_cycles': 0,
            'haack_executions': 0,
            'context_switches': 0,
            'errors': 0,
            'start_time': time.time()
        }
        
        print(f"[BRIDGE] Initialized Singularis↔HaackLang bridge")
        print(f"[BRIDGE] Modules directory: {haack_modules_dir}")
        print(f"[BRIDGE] Beat interval: {beat_interval}s ({1/beat_interval:.1f} Hz)")
    
    def load_all_modules(self) -> int:
        """
        Load all .haack modules from the modules directory.
        
        Returns:
            Number of modules loaded
        """
        if not self.haack_modules_dir.exists():
            print(f"[BRIDGE] Warning: Modules directory not found: {self.haack_modules_dir}")
            return 0
        
        haack_files = list(self.haack_modules_dir.glob("*.haack"))
        
        print(f"[BRIDGE] Found {len(haack_files)} .haack modules")
        
        for haack_file in haack_files:
            if self.runtime.load_module(haack_file):
                self.loaded_modules.append(haack_file.stem)
        
        print(f"[BRIDGE] Loaded {len(self.loaded_modules)} modules successfully")
        return len(self.loaded_modules)
    
    def register_python_callback(self, name: str, callback: Callable):
        """
        Register a Python function that can be called from HaackLang.
        
        Example:
            def gemini_vision_threat(game_state):
                return gemini_vision_analysis(game_state)
            
            bridge.register_python_callback('gemini_vision_threat', gemini_vision_threat)
        
        Args:
            name: Function name as it appears in .haack code
            callback: Python callable
        """
        self.runtime.register_python_callback(name, callback)
    
    def update_game_state(self, game_state_dict: Dict[str, Any]):
        """
        Update game state and switch HaackLang context if needed.
        
        Args:
            game_state_dict: Dictionary with game state fields
        """
        # Update state
        old_context = self.game_state.get_context()
        
        self.game_state.in_combat = game_state_dict.get('in_combat', False)
        self.game_state.in_menu = game_state_dict.get('in_menu', False)
        self.game_state.in_dialogue = game_state_dict.get('in_dialogue', False)
        self.game_state.in_exploration = not (
            self.game_state.in_combat or 
            self.game_state.in_menu or 
            self.game_state.in_dialogue
        )
        
        # Switch context if changed
        new_context = self.game_state.get_context()
        if new_context != old_context:
            self.runtime.switch_context(new_context)
            self.stats['context_switches'] += 1
            print(f"[BRIDGE] Context switch: {old_context} → {new_context}")
    
    def update_truthvalue(self, name: str, track: str, value: float):
        """
        Update a HaackLang truthvalue from Python subsystem.
        
        Args:
            name: TruthValue name
            track: Track name
            value: Value (0.0-1.0)
        """
        self.runtime.set_truthvalue(name, track, value)
    
    def get_truthvalue(self, name: str, track: Optional[str] = None) -> Any:
        """
        Get a HaackLang truthvalue.
        
        Args:
            name: TruthValue name
            track: Specific track (None = all tracks)
        
        Returns:
            Value or dict of values
        """
        return self.runtime.get_truthvalue(name, track)
    
    async def cycle(
        self,
        perception: Dict[str, Any],
        subsystem_outputs: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Execute one cognitive cycle through HaackLang.
        
        This is the main integration point called from Singularis main loop.
        
        Args:
            perception: Current perception data
            subsystem_outputs: Dict of subsystem_name → value
        
        Returns:
            Dictionary with:
                - action: Recommended action (if any)
                - truthvalues: All truthvalue states
                - active_tracks: Which tracks fired this cycle
                - metadata: Cycle metadata
        """
        start_time = time.time()
        
        # Advance beat
        self.runtime.advance_beat()
        self.stats['total_cycles'] += 1
        
        # Get active tracks
        active_tracks = self.runtime.get_active_tracks()
        
        # Update truthvalues from subsystem outputs
        for subsystem_name, value in subsystem_outputs.items():
            # Infer track from subsystem name
            track = self._infer_track_from_subsystem(subsystem_name)
            
            # Update truthvalue
            tv_name = self._subsystem_to_truthvalue(subsystem_name)
            self.update_truthvalue(tv_name, track, value)
        
        # Execute appropriate HaackLang module based on context
        module_name = self._get_module_for_context()
        
        result = None
        if module_name and module_name in self.loaded_modules:
            result = self.runtime.execute(
                module=module_name,
                context=self.game_state.get_context(),
                inputs={
                    'perception': perception,
                    'game_state': self.game_state.__dict__
                }
            )
            
            self.stats['haack_executions'] += 1
            
            if not result.success:
                self.stats['errors'] += len(result.errors)
        
        # Build response
        cycle_time = time.time() - start_time
        
        return {
            'action': result.action if result else None,
            'truthvalues': self.runtime.interpreter.truthvalues,
            'active_tracks': active_tracks,
            'metadata': {
                'beat': self.runtime.scheduler.global_beat,
                'context': self.game_state.get_context(),
                'cycle_time': cycle_time,
                'success': result.success if result else False,
                'errors': result.errors if result else []
            }
        }
    
    def _infer_track_from_subsystem(self, subsystem_name: str) -> str:
        """
        Map subsystem name to track name.
        
        Args:
            subsystem_name: Name of Singularis subsystem
        
        Returns:
            Track name
        """
        # Mapping based on subsystem naming conventions
        if 'perception' in subsystem_name or 'vision' in subsystem_name:
            return 'perception'
        elif 'reflex' in subsystem_name or 'emergency' in subsystem_name:
            return 'reflex'
        elif 'strategic' in subsystem_name or 'planner' in subsystem_name:
            return 'strategic'
        elif 'emotion' in subsystem_name or 'feeling' in subsystem_name:
            return 'intuition'
        elif 'learning' in subsystem_name or 'memory' in subsystem_name:
            return 'learning'
        elif 'reflection' in subsystem_name or 'meta' in subsystem_name:
            return 'meta'
        else:
            return 'perception'  # Default
    
    def _subsystem_to_truthvalue(self, subsystem_name: str) -> str:
        """
        Map subsystem name to truthvalue name.
        
        Args:
            subsystem_name: Subsystem identifier
        
        Returns:
            TruthValue name
        """
        # Simple mapping - could be more sophisticated
        return subsystem_name.replace('_', '.')
    
    def _get_module_for_context(self) -> Optional[str]:
        """
        Get which .haack module to execute based on current context.
        
        Returns:
            Module name or None
        """
        context = self.game_state.get_context()
        
        # Map contexts to modules
        context_to_module = {
            'combat': 'combat_decision',
            'exploration': 'exploration_decision',
            'menu': 'menu_decision',
            'dialogue': 'dialogue_decision'
        }
        
        module = context_to_module.get(context)
        
        # Fallback to generic decision module
        if not module or module not in self.loaded_modules:
            if 'decision' in self.loaded_modules:
                return 'decision'
        
        return module
    
    def get_stats(self) -> Dict[str, Any]:
        """Get bridge statistics."""
        uptime = time.time() - self.stats['start_time']
        
        return {
            **self.stats,
            'loaded_modules': len(self.loaded_modules),
            'uptime': uptime,
            'cycles_per_second': self.stats['total_cycles'] / uptime if uptime > 0 else 0,
            'runtime_stats': self.runtime.get_stats()
        }
    
    def print_status(self):
        """Print detailed status."""
        print("\n" + "="*70)
        print("Singularis↔HaackLang Bridge Status")
        print("="*70)
        
        stats = self.get_stats()
        
        print(f"\nModules: {stats['loaded_modules']} loaded")
        print(f"  {', '.join(self.loaded_modules)}")
        
        print(f"\nExecution:")
        print(f"  Total Cycles: {stats['total_cycles']}")
        print(f"  HaackLang Executions: {stats['haack_executions']}")
        print(f"  Cycles/Second: {stats['cycles_per_second']:.2f}")
        
        print(f"\nCurrent State:")
        print(f"  Beat: {self.runtime.scheduler.global_beat}")
        print(f"  Context: {self.game_state.get_context()}")
        print(f"  Active Tracks: {', '.join(self.runtime.get_active_tracks())}")
        
        print(f"\nGame State:")
        print(f"  Combat: {self.game_state.in_combat}")
        print(f"  Menu: {self.game_state.in_menu}")
        print(f"  Dialogue: {self.game_state.in_dialogue}")
        print(f"  Exploration: {self.game_state.in_exploration}")
        
        print(f"\nStatistics:")
        print(f"  Context Switches: {stats['context_switches']}")
        print(f"  Errors: {stats['errors']}")
        print(f"  Uptime: {stats['uptime']:.1f}s")
        
        print("="*70 + "\n")
        
        # Print beat schedule
        print(self.runtime.scheduler.get_beat_phase_diagram(20))
