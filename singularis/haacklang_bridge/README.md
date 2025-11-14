# HaackLang↔Singularis Python FFI Bridge

This module provides the integration layer between Singularis AGI (Python) and HaackLang cognitive modules (.haack files).

## Components

### `runtime.py`
Core HaackLang runtime environment (HLVM):
- **BeatScheduler**: Global Beat Scheduler managing temporal rhythms
- **HaackLangRuntime**: Main runtime for executing .haack modules

### `decorators.py`
Python decorators for seamless integration:
- `@haack_track`: Map Python class/function to a track
- `@haack_truthvalue`: Map function output to truthvalue
- `@haack_context`: Map class to cognitive context
- `@haack_guard`: Map method to guard condition

### `bridge.py`
Main integration bridge:
- **SingularisHaackBridge**: Coordinates Singularis↔HaackLang communication
- **GameStateMapping**: Maps game state to HaackLang contexts
- Beat-gated execution integration

### `truthvalue_sync.py` (planned)
TruthValue synchronization protocol between Python and HaackLang.

## Quick Start

```python
from haacklang_bridge import SingularisHaackBridge
from pathlib import Path

# Initialize bridge
bridge = SingularisHaackBridge(
    haack_modules_dir=Path('cognitive_modules'),
    beat_interval=0.1  # 10 Hz
)

# Load .haack modules
bridge.load_all_modules()

# Register Python callbacks
bridge.register_python_callback('gemini_vision_threat', gemini_vision)

# Execute cognitive cycle
result = await bridge.cycle(
    perception={'game_state': state},
    subsystem_outputs={'perception.danger': 0.9}
)

if result['action']:
    execute_action(result['action'])
```

## Decorator Usage

### Track Mapping
```python
@haack_track('perception', period=1, logic='classical')
class PerceptionSubsystem:
    def process(self, game_state):
        return threat_level
```

### TruthValue Updates
```python
@haack_truthvalue('danger', track='perception')
def detect_threats(game_state):
    return 0.9  # Automatically syncs to HaackLang
```

### Context Definition
```python
@haack_context('combat', priority=['reflex', 'perception', 'strategic'])
class CombatMode:
    def enter(self):
        self.active = True
```

### Guard Conditions
```python
@haack_guard('reflex', condition='threat_level > 0.8')
def emergency_dodge(self):
    return Action.DODGE
```

## Architecture

```
Python Subsystems
        ↓
    Decorators (@haack_track, @haack_truthvalue)
        ↓
SingularisHaackBridge
        ↓
  HaackLangRuntime (HLVM)
        ↓
   BeatScheduler (GBS)
        ↓
  .haack Cognitive Modules
```

## Track System

Default tracks:
- **perception** (period 1, classical) - Fast sensory processing
- **reflex** (period 1, classical) - Immediate responses  
- **strategic** (period 3, fuzzy) - Deliberate planning
- **intuition** (period 7, paraconsistent) - Emotional/subconscious
- **learning** (period 10, fuzzy) - Pattern learning
- **reflection** (period 10, fuzzy) - Self-reflection
- **meta** (period 20, fuzzy) - Meta-cognition

## Context System

Default contexts:
- **combat** - Fast reflexes, trust perception
- **exploration** - Balanced assessment, trust strategy
- **menu** - Deliberate choices, no reflexes
- **dialogue** - Strategic conversation
- **survival** - Emergency mode, perception priority

## Examples

See `../skyrim/Haacklang/examples/singularis_integration_example.py`

## Documentation

- Full specification: `../../SINGULARIS_HAACKLANG_INTEGRATION_SPEC.md`
- Integration guide: `../../HAACKLANG_INTEGRATION_GUIDE.md`
- HaackLang spec: `../skyrim/Haacklang/haack_lang_specification.md`

## Status

**Phase 1**: Core HLVM ✅ (Partially Complete)  
**Phase 2**: Singularis Integration 🔄 (Next)  
**Phase 3**: Cognitive Module Migration ⏳ (Planned)  
**Phase 4**: Self-Modification ⏳ (Future)

## Requirements

- Python 3.8+
- HaackLang compiler (included in `../skyrim/Haacklang/src/`)

## Testing

```bash
# Run integration example
cd ../skyrim/Haacklang/examples
python singularis_integration_example.py
```

## License

Part of Singularis AGI project
