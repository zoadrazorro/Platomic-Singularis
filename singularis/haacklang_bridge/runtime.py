"""
HaackLang Runtime - Core execution engine for HaackLang modules.

Implements:
- Global Beat Scheduler (GBS)
- Track Manager
- Context Engine
- TruthValue/BoolRhythm Management
- Polylogical ALUs
"""

import sys
import time
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Callable
from dataclasses import dataclass, field
from enum import Enum

# Import HaackLang compiler components
sys.path.append(str(Path(__file__).parent.parent / 'skyrim' / 'Haacklang' / 'src'))
from haackc.runtime import Track, TruthValue, Context, LogicType
from haackc.parser import Parser
from haackc.lexer import Lexer
from haackc.interpreter import Interpreter


class BeatScheduler:
    """
    Global Beat Scheduler (GBS) - Manages temporal rhythm across all tracks.
    
    The GBS is the heart of HaackLang's polyrhythmic execution model.
    It determines which tracks fire on each global beat.
    """
    
    def __init__(self, beat_interval: float = 0.1):
        """
        Initialize beat scheduler.
        
        Args:
            beat_interval: Seconds between beats (default: 0.1s = 10Hz)
        """
        self.beat_interval = beat_interval
        self.global_beat = 0
        self.start_time = time.time()
        self.paused = False
        
        # Track registry
        self.tracks: Dict[str, Track] = {}
        
        # Beat history
        self.beat_history: List[Dict[str, Any]] = []
        self.max_history = 1000
    
    def register_track(self, track: Track):
        """Register a track with the scheduler."""
        self.tracks[track.name] = track
        print(f"[GBS] Registered {track}")
    
    def advance_beat(self, external_beat: Optional[int] = None):
        """
        Advance the global beat counter.
        
        Args:
            external_beat: If provided, sync to external beat counter
        """
        if external_beat is not None:
            self.global_beat = external_beat
        else:
            self.global_beat += 1
        
        # Record beat
        active_tracks = self.get_active_tracks()
        self.beat_history.append({
            'beat': self.global_beat,
            'timestamp': time.time(),
            'active_tracks': [t.name for t in active_tracks]
        })
        
        # Limit history
        if len(self.beat_history) > self.max_history:
            self.beat_history.pop(0)
        
        # Advance all tracks
        for track in self.tracks.values():
            track.advance()
    
    def get_active_tracks(self, beat: Optional[int] = None) -> List[Track]:
        """
        Get which tracks fire on this beat.
        
        Args:
            beat: Beat number to check (default: current global beat)
        
        Returns:
            List of tracks that fire on this beat
        """
        if beat is None:
            beat = self.global_beat
        
        return [
            track for track in self.tracks.values()
            if track.is_active(beat)
        ]
    
    def get_beat_phase_diagram(self, num_beats: int = 20) -> str:
        """
        Generate ASCII diagram showing which tracks fire on each beat.
        
        Args:
            num_beats: Number of beats to show
        
        Returns:
            ASCII art diagram
        """
        diagram = []
        diagram.append(f"Beat Schedule (next {num_beats} beats):")
        diagram.append("=" * 60)
        
        # Header
        header = "Beat |"
        for track_name in sorted(self.tracks.keys()):
            header += f" {track_name[:8]:8s} |"
        diagram.append(header)
        diagram.append("-" * 60)
        
        # Rows
        for beat in range(self.global_beat, self.global_beat + num_beats):
            row = f"{beat:4d} |"
            for track_name in sorted(self.tracks.keys()):
                track = self.tracks[track_name]
                if track.is_active(beat):
                    row += f"    ▀▀    |"
                else:
                    row += f"          |"
            diagram.append(row)
        
        return "\n".join(diagram)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get scheduler statistics."""
        return {
            'global_beat': self.global_beat,
            'num_tracks': len(self.tracks),
            'uptime': time.time() - self.start_time,
            'beats_per_second': self.global_beat / (time.time() - self.start_time) if time.time() > self.start_time else 0,
            'paused': self.paused
        }


@dataclass
class ExecutionResult:
    """Result from executing a HaackLang module."""
    success: bool
    action: Optional[str] = None
    truthvalues: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    execution_time: float = 0.0


class HaackLangRuntime:
    """
    HaackLang Runtime Environment (HLVM).
    
    Manages:
    - Beat scheduler
    - Track execution
    - Context switching
    - TruthValue synchronization
    - Python↔HaackLang FFI
    """
    
    def __init__(self, beat_interval: float = 0.1):
        """
        Initialize HaackLang runtime.
        
        Args:
            beat_interval: Seconds between beats
        """
        self.scheduler = BeatScheduler(beat_interval)
        self.interpreter = Interpreter()
        
        # Contexts
        self.contexts: Dict[str, Context] = {}
        self.current_context: Optional[str] = None
        
        # Python callback registry
        self.python_callbacks: Dict[str, Callable] = {}
        
        # Loaded modules
        self.loaded_modules: Dict[str, Any] = {}
        
        # Statistics
        self.stats = {
            'modules_loaded': 0,
            'total_executions': 0,
            'total_beats': 0,
            'errors': 0
        }
        
        print("[HLVM] HaackLang Runtime initialized")
    
    def load_module(self, module_path: Path) -> bool:
        """
        Load and compile a .haack module.
        
        Args:
            module_path: Path to .haack file
        
        Returns:
            True if successful
        """
        try:
            source = module_path.read_text()
            
            # Lex
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            
            # Parse
            parser = Parser(tokens)
            ast = parser.parse()
            
            # Store compiled module
            module_name = module_path.stem
            self.loaded_modules[module_name] = {
                'path': module_path,
                'ast': ast,
                'tokens': tokens,
                'loaded_at': time.time()
            }
            
            # Extract and register tracks from AST
            self._extract_tracks_from_ast(ast)
            
            # Extract and register contexts
            self._extract_contexts_from_ast(ast)
            
            self.stats['modules_loaded'] += 1
            print(f"[HLVM] Loaded module: {module_name}")
            
            return True
            
        except Exception as e:
            print(f"[HLVM] Failed to load module {module_path}: {e}")
            self.stats['errors'] += 1
            return False
    
    def _extract_tracks_from_ast(self, ast):
        """Extract track declarations from AST and register with scheduler."""
        # This would need to traverse the AST looking for TrackDeclaration nodes
        # For now, we'll create default tracks
        
        # Default tracks for Singularis
        default_tracks = [
            Track('perception', period=1, logic=LogicType.CLASSICAL),
            Track('reflex', period=1, logic=LogicType.CLASSICAL),
            Track('strategic', period=3, logic=LogicType.FUZZY),
            Track('intuition', period=7, logic=LogicType.PARACONSISTENT),
            Track('learning', period=10, logic=LogicType.FUZZY),
            Track('reflection', period=10, logic=LogicType.FUZZY),
            Track('meta', period=20, logic=LogicType.FUZZY),
        ]
        
        for track in default_tracks:
            if track.name not in self.scheduler.tracks:
                self.scheduler.register_track(track)
                self.interpreter.tracks[track.name] = track
    
    def _extract_contexts_from_ast(self, ast):
        """Extract context declarations from AST."""
        # Default contexts for Singularis
        default_contexts = [
            Context('perception', logic=LogicType.CLASSICAL, track='perception'),
            Context('combat', logic=LogicType.CLASSICAL, track='reflex'),
            Context('exploration', logic=LogicType.FUZZY, track='strategic'),
            Context('menu', logic=LogicType.FUZZY, track='strategic'),
            Context('dialogue', logic=LogicType.FUZZY, track='strategic'),
            Context('learning', logic=LogicType.FUZZY, track='learning'),
            Context('metacognition', logic=LogicType.FUZZY, track='meta'),
        ]
        
        for context in default_contexts:
            if context.name not in self.contexts:
                self.contexts[context.name] = context
    
    def execute(
        self,
        module: str,
        context: Optional[str] = None,
        inputs: Optional[Dict[str, Any]] = None
    ) -> ExecutionResult:
        """
        Execute a HaackLang module.
        
        Args:
            module: Module name (without .haack)
            context: Context to execute in (default: current)
            inputs: Input variables to pass to module
        
        Returns:
            ExecutionResult with action and truthvalues
        """
        start_time = time.time()
        result = ExecutionResult(success=False)
        
        try:
            # Get module
            if module not in self.loaded_modules:
                result.errors.append(f"Module not loaded: {module}")
                return result
            
            module_data = self.loaded_modules[module]
            ast = module_data['ast']
            
            # Set context
            if context:
                self.current_context = context
            
            # Set inputs in interpreter
            if inputs:
                for name, value in inputs.items():
                    self.interpreter.set_variable(name, value)
            
            # Register Python callbacks with interpreter
            self.interpreter.python_callbacks = self.python_callbacks
            
            # Execute AST
            self.interpreter.interpret(ast)
            
            # Extract results
            result.truthvalues = {
                name: tv.to_dict()
                for name, tv in self.interpreter.truthvalues.items()
            }
            
            # Check for action result
            if hasattr(self.interpreter, 'result_action'):
                result.action = self.interpreter.result_action
            
            result.success = True
            self.stats['total_executions'] += 1
            
        except Exception as e:
            result.errors.append(str(e))
            result.success = False
            self.stats['errors'] += 1
        
        result.execution_time = time.time() - start_time
        result.metadata = {
            'module': module,
            'context': self.current_context,
            'beat': self.scheduler.global_beat
        }
        
        return result
    
    def register_python_callback(self, name: str, callback: Callable):
        """
        Register a Python function that can be called from HaackLang.
        
        Args:
            name: Function name as it appears in .haack code
            callback: Python callable
        """
        self.python_callbacks[name] = callback
        print(f"[HLVM] Registered Python callback: {name}")
    
    def set_truthvalue(self, name: str, track: str, value: float):
        """
        Set a truthvalue from Python.
        
        Args:
            name: TruthValue name
            track: Track name
            value: Value to set (0.0-1.0)
        """
        if name not in self.interpreter.truthvalues:
            # Create new truthvalue
            tv = TruthValue(self.interpreter.tracks, initial_value=0.0)
            self.interpreter.truthvalues[name] = tv
        
        self.interpreter.truthvalues[name].set(track, value)
    
    def get_truthvalue(self, name: str, track: Optional[str] = None) -> Any:
        """
        Get a truthvalue from HaackLang.
        
        Args:
            name: TruthValue name
            track: Specific track (default: all tracks)
        
        Returns:
            Value or dict of values
        """
        if name not in self.interpreter.truthvalues:
            return None
        
        tv = self.interpreter.truthvalues[name]
        
        if track:
            return tv.get(track)
        else:
            return tv.to_dict()
    
    def switch_context(self, context_name: str):
        """
        Switch to a different cognitive context.
        
        Args:
            context_name: Name of context to switch to
        """
        if context_name in self.contexts:
            self.current_context = context_name
            print(f"[HLVM] Switched to context: {context_name}")
        else:
            print(f"[HLVM] Warning: Unknown context: {context_name}")
    
    def advance_beat(self):
        """Advance the global beat counter."""
        self.scheduler.advance_beat()
        self.stats['total_beats'] += 1
    
    def get_active_tracks(self) -> List[str]:
        """Get names of tracks active on current beat."""
        return [t.name for t in self.scheduler.get_active_tracks()]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get runtime statistics."""
        return {
            **self.stats,
            'scheduler': self.scheduler.get_stats(),
            'num_truthvalues': len(self.interpreter.truthvalues),
            'num_contexts': len(self.contexts),
            'current_context': self.current_context
        }
    
    def print_status(self):
        """Print current runtime status."""
        print("\n" + "="*70)
        print("HaackLang Runtime Status")
        print("="*70)
        
        stats = self.get_stats()
        print(f"Beat: {self.scheduler.global_beat}")
        print(f"Active Tracks: {', '.join(self.get_active_tracks())}")
        print(f"Current Context: {self.current_context}")
        print(f"Loaded Modules: {stats['modules_loaded']}")
        print(f"Total Executions: {stats['total_executions']}")
        print(f"TruthValues: {stats['num_truthvalues']}")
        print(f"Errors: {stats['errors']}")
        print("="*70 + "\n")
