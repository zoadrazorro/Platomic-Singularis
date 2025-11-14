"""
HaackLang↔Singularis Python FFI Bridge

This module provides the integration layer between Singularis AGI (Python)
and HaackLang cognitive modules (.haack files).

Key Components:
- Track decorators for subsystem→track mapping
- TruthValue synchronization protocol
- Context switching based on game state
- Beat-gated execution integration
"""

from .runtime import HaackLangRuntime, BeatScheduler
from .decorators import haack_track, haack_truthvalue, haack_context, haack_guard
from .bridge import SingularisHaackBridge
from .truthvalue_sync import TruthValueSync

__version__ = "1.0.0"

__all__ = [
    'HaackLangRuntime',
    'BeatScheduler',
    'haack_track',
    'haack_truthvalue',
    'haack_context',
    'haack_guard',
    'SingularisHaackBridge',
    'TruthValueSync',
]
