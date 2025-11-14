# HaackLang Integration Guide for Singularis

**Version**: 1.0  
**Last Updated**: November 14, 2025

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Quick Start](#quick-start)
4. [Integration Patterns](#integration-patterns)
5. [Cognitive Modules](#cognitive-modules)
6. [Python FFI](#python-ffi)
7. [Beat-Gated Execution](#beat-gated-execution)
8. [Context Switching](#context-switching)
9. [TruthValue Synchronization](#truthvalue-synchronization)
10. [Examples](#examples)
11. [Troubleshooting](#troubleshooting)
12. [Roadmap](#roadmap)

---

## Overview

HaackLang provides formal polyrhythmic, polylogical orchestration for Singularis's 53+ subsystems. Instead of ad-hoc Python coordination, HaackLang gives you:

✅ **Formal temporal guarantees** - Tracks ensure subsystems synchronize correctly  
✅ **Declarative modal switching** - Contexts replace if/else spaghetti  
✅ **Type-safe truth propagation** - BoolRhythm tracks truth across multiple logics  
✅ **Automatic coherence** - Built-in `@coh` operators measure agreement  
✅ **Contradiction handling** - Paraconsistent tracks preserve contradictions safely  

### The Problem HaackLang Solves

**Before** (Current Singularis):
```python
# Manual coordination across files
danger_perception = gemini_vision()  # perception.py
danger_strategic = planner.assess()   # strategic_planner.py
danger_emotional = emotion_system()   # emotion_integration.py

# Manual conflict resolution
if survival_mode:
    danger = danger_perception
else:
    danger = weighted_average([...])  # Hope they're synchronized!
```

**After** (With HaackLang):
```haack
# danger_evaluation.haack - single source of truth
truthvalue danger

context perception {
    danger.perception = gemini_vision_threat()
}

context strategic {
    danger.strategic = assess_long_term_risk()
}

context emotional {
    danger.intuition = fear_level()
}

# Automatic coherence checking
if @coh(danger) < 0.4 {
    enter context survival  # Formal fallback
}
```

---

## Architecture

### System Layers

```
┌─────────────────────────────────────────────┐
│     Singularis Python Shell                │
│  • Game I/O                                 │
│  • API clients (OpenAI, Gemini, etc.)      │
│  • Monitoring & telemetry                   │
└──────────────────┬──────────────────────────┘
                   │ FFI Bridge
                   ↓
┌─────────────────────────────────────────────┐
│     HaackLang Runtime (HLVM)                │
│  • Global Beat Scheduler (GBS)             │
│  • Track Manager (7 default tracks)        │
│  • Context Engine (CAL)                    │
│  • BoolRhythm/TruthValue Manager           │
│  • Polylogical ALUs                        │
└──────────────────┬──────────────────────────┘
                   │ Executes
                   ↓
┌─────────────────────────────────────────────┐
│    .haack Cognitive Modules                 │
│  • danger_evaluation.haack                  │
│  • action_selection.haack                   │
│  • coherence_monitoring.haack               │
└─────────────────────────────────────────────┘
```

### Key Components

**Global Beat Scheduler (GBS)**  
- Manages temporal rhythms across all tracks
- Determines which tracks fire on each beat
- Provides formal synchronization guarantees

**Tracks (7 Default)**  
- `perception` (period 1, classical) - Fast sensory processing
- `reflex` (period 1, classical) - Immediate responses
- `strategic` (period 3, fuzzy) - Deliberate planning
- `intuition` (period 7, paraconsistent) - Emotional/subconscious
- `learning` (period 10, fuzzy) - Pattern learning
- `reflection` (period 10, fuzzy) - Self-reflection
- `meta` (period 20, fuzzy) - Meta-cognition

**Contexts**  
- `combat` - Fast reflexes, trust perception
- `exploration` - Balanced assessment, trust strategy
- `menu` - Deliberate choices, no reflexes
- `dialogue` - Strategic conversation
- `survival` - Emergency mode, perception priority

---

## Quick Start

### 1. Installation

The HaackLang bridge is already integrated into Singularis:

```bash
# No additional installation needed
# Bridge located at: singularis/haacklang_bridge/
```

### 2. Load HaackLang Modules

```python
from singularis.haacklang_bridge import SingularisHaackBridge
from pathlib import Path

# Initialize bridge
bridge = SingularisHaackBridge(
    haack_modules_dir=Path('singularis/skyrim/Haacklang/cognitive_modules'),
    beat_interval=0.1  # 10 Hz
)

# Load all .haack modules
bridge.load_all_modules()
```

### 3. Register Python Callbacks

```python
# Register functions that .haack modules can call
bridge.register_python_callback('gemini_vision_threat', gemini_vision_threat)
bridge.register_python_callback('assess_long_term_risk', planner.assess_risk)
bridge.register_python_callback('fear_level', emotion_system.get_fear)
```

### 4. Execute Cognitive Cycle

```python
async def main_loop():
    while True:
        # Gather subsystem outputs
        subsystem_outputs = {
            'perception.danger': perception.detect_threats(game_state),
            'strategic.danger': planner.assess_risk(game_state),
            'emotion.fear': emotion_system.get_fear(game_state)
        }
        
        # Execute through HaackLang
        result = await bridge.cycle(
            perception={'game_state': game_state},
            subsystem_outputs=subsystem_outputs
        )
        
        # Use recommended action
        if result['action']:
            execute_action(result['action'])
        
        await asyncio.sleep(bridge.beat_interval)
```

---

## Integration Patterns

### Pattern 1: Decorator-Based Integration

Use decorators to map Python subsystems to HaackLang constructs:

```python
from haacklang_bridge.decorators import haack_track, haack_truthvalue

@haack_track('perception', period=1, logic='classical')
class PerceptionSubsystem:
    
    @haack_truthvalue('danger', track='perception')
    def detect_threats(self, game_state):
        return gemini_vision_analysis(game_state)
```

### Pattern 2: Manual TruthValue Updates

Directly update HaackLang truthvalues from Python:

```python
# Update danger truthvalue on perception track
bridge.update_truthvalue('danger', 'perception', 0.9)

# Query danger across all tracks
danger_values = bridge.get_truthvalue('danger')  # Returns dict
```

### Pattern 3: Context-Based Execution

Let HaackLang handle context switching:

```python
# Update game state
bridge.update_game_state({
    'in_combat': True,
    'in_menu': False,
    'in_dialogue': False
})

# HaackLang automatically switches to 'combat' context
# and adjusts track priorities accordingly
```

---

## Cognitive Modules

### danger_evaluation.haack

**Purpose**: Multi-modal danger assessment  
**Tracks**: perception (1), strategic (3), intuition (7)  
**Contexts**: perception, strategic, emotional, survival, exploration, combat

**Key Features**:
- Fast perceptual threat detection
- Slow strategic risk assessment
- Emotional/intuitive danger sensing
- Automatic coherence checking
- Context-appropriate responses

**Usage**:
```python
result = bridge.runtime.execute(
    module='danger_evaluation',
    context='combat',
    inputs={'game_state': current_state}
)

if result.action == 'emergency_response':
    execute_dodge()
```

### action_selection.haack

**Purpose**: Polyrhythmic action selection  
**Tracks**: reflex (1), deliberate (3), learning (10)  
**Contexts**: reflex, combat, exploration, menu

**Key Features**:
- Immediate reflex actions (dodge, heal, flee)
- Tactical combat decisions
- Learned policies from RL
- Q-value updates from outcomes

**Usage**:
```python
result = bridge.runtime.execute(
    module='action_selection',
    context='combat',
    inputs={
        'dodge_needed': 0.8,
        'attack_opportunity': 0.6
    }
)

action = result.action  # e.g., 'power_attack'
```

### coherence_monitoring.haack

**Purpose**: Meta-cognitive coherence assessment  
**Tracks**: meta (20)  
**Contexts**: metacognition, lumen, double_helix

**Key Features**:
- 4D coherence (integration + temporal + causal + predictive)
- Lumen balance (onticum, structurale, participatum)
- Double helix integration (analytical ↔ intuitive)
- Subsystem conflict resolution

**Usage**:
```python
result = bridge.runtime.execute(
    module='coherence_monitoring',
    context='metacognition',
    inputs={}
)

if result.action == 'emergency_coherence_recovery':
    trigger_meta_intervention()
```

---

## Python FFI

### Calling Python from HaackLang

In `.haack` files, use `python_call()`:

```haack
# danger_evaluation.haack
danger.perception = python_call("gemini_vision_threat", game_state)
```

Register the Python function:

```python
def gemini_vision_threat(game_state):
    return gemini_vision.analyze(game_state)

bridge.register_python_callback('gemini_vision_threat', gemini_vision_threat)
```

### Calling HaackLang from Python

Execute modules:

```python
result = bridge.runtime.execute(
    module='danger_evaluation',
    context='combat',
    inputs={'game_state': state}
)
```

Query truthvalues:

```python
# Get danger on perception track
danger_perception = bridge.get_truthvalue('danger', 'perception')

# Get danger across all tracks
danger_all = bridge.get_truthvalue('danger')  # Dict
```

---

## Beat-Gated Execution

### Understanding Beats

A **beat** is the fundamental time unit in HaackLang. The Global Beat Scheduler (GBS) increments the beat counter and determines which tracks fire.

**Default Configuration**:
- Beat interval: 0.1s (10 Hz)
- `perception` track: fires every beat (10 Hz)
- `strategic` track: fires every 3 beats (3.33 Hz)
- `meta` track: fires every 20 beats (0.5 Hz)

### Beat Schedule Visualization

```
Beat | perception | strategic | intuition | meta
-----+------------+-----------+-----------+------
  0  |     ▀▀     |     ▀▀    |           |  ▀▀
  1  |     ▀▀     |           |           |
  2  |     ▀▀     |           |           |
  3  |     ▀▀     |     ▀▀    |           |
  4  |     ▀▀     |           |           |
  5  |     ▀▀     |           |           |
  6  |     ▀▀     |     ▀▀    |           |
  7  |     ▀▀     |           |     ▀▀    |
  8  |     ▀▀     |           |           |
  9  |     ▀▀     |     ▀▀    |           |
 10  |     ▀▀     |           |           |
```

### Integrating with Singularis Main Loop

```python
async def singularis_main_loop():
    global_beat = 0
    
    while True:
        # Advance beat
        bridge.runtime.advance_beat()
        global_beat += 1
        
        # Get active tracks this beat
        active_tracks = bridge.get_active_tracks()
        
        # Execute appropriate modules
        if 'perception' in active_tracks:
            # Fast perceptual processing
            pass
        
        if 'strategic' in active_tracks:
            # Strategic planning
            pass
        
        if 'meta' in active_tracks:
            # Meta-cognitive assessment
            coherence_result = bridge.runtime.execute(
                module='coherence_monitoring',
                context='metacognition'
            )
        
        # Sleep until next beat
        await asyncio.sleep(bridge.beat_interval)
```

---

## Context Switching

### Automatic Context Switching

The bridge automatically switches contexts based on game state:

```python
# Update game state
bridge.update_game_state({
    'in_combat': True,
    'in_menu': False,
    'in_dialogue': False
})

# Bridge switches to 'combat' context automatically
```

### Context Priority

Each context defines track priorities:

```haack
context combat {
    priority reflex > perception > strategic
    # Reflex actions take precedence over strategic planning
}

context exploration {
    priority strategic > perception > intuition
    # Strategic planning takes precedence
}
```

### Manual Context Switching

```python
# Force context switch
bridge.runtime.switch_context('survival')
```

---

## TruthValue Synchronization

### Python → HaackLang

Update truthvalues from Python subsystems:

```python
# Direct update
bridge.update_truthvalue('danger', 'perception', 0.9)

# Via decorator (automatic)
@haack_truthvalue('danger', track='perception')
def detect_threats(game_state):
    return 0.9
```

### HaackLang → Python

Query truthvalues from HaackLang:

```python
# Single track
perception_danger = bridge.get_truthvalue('danger', 'perception')

# All tracks
danger_all = bridge.get_truthvalue('danger')
# Returns: {'perception': 0.9, 'strategic': 0.6, 'intuition': 0.7}
```

### Cross-Track Propagation

HaackLang automatically propagates truthvalues across tracks according to each track's logic:

```haack
truthvalue danger

# Set on perception track
danger.perception = 0.9

# Automatically available on all tracks
# Each track may transform the value according to its logic
```

---

## Examples

### Example 1: Basic Integration

See `singularis/skyrim/Haacklang/examples/singularis_integration_example.py`

Demonstrates:
- Loading HaackLang modules
- Registering Python callbacks
- Running cognitive cycles
- Multiple scenarios (exploration, combat, emergency)

**Run it**:
```bash
cd singularis/skyrim/Haacklang/examples
python singularis_integration_example.py
```

### Example 2: Danger Evaluation

```python
# Python side
from haacklang_bridge import SingularisHaackBridge

bridge = SingularisHaackBridge(modules_dir, beat_interval=0.1)
bridge.load_all_modules()

# Register callbacks
bridge.register_python_callback('gemini_vision_threat', gemini_threat)
bridge.register_python_callback('assess_long_term_risk', strategic_risk)
bridge.register_python_callback('fear_level', emotion_fear)

# Execute
result = await bridge.cycle(
    perception={'game_state': state},
    subsystem_outputs={
        'perception.danger': 0.9,
        'strategic.danger': 0.6,
        'emotion.fear': 0.7
    }
)

if result['action'] == 'emergency_response':
    execute_dodge()
```

---

## Troubleshooting

### Issue: Modules Not Loading

**Symptom**: `Module not loaded: danger_evaluation`

**Solution**:
```python
# Check modules directory exists
print(f"Modules dir: {bridge.haack_modules_dir}")
print(f"Exists: {bridge.haack_modules_dir.exists()}")

# Check .haack files
files = list(bridge.haack_modules_dir.glob('*.haack'))
print(f"Found {len(files)} .haack files")
```

### Issue: Python Callbacks Not Found

**Symptom**: `.haack code calls python_call('function_name') but fails`

**Solution**:
```python
# Verify callback is registered
print(bridge.runtime.python_callbacks.keys())

# Register if missing
bridge.register_python_callback('function_name', function)
```

### Issue: Tracks Not Firing

**Symptom**: Certain tracks never execute

**Solution**:
```python
# Check beat schedule
print(bridge.runtime.scheduler.get_beat_phase_diagram(20))

# Verify track registration
print(bridge.runtime.scheduler.tracks.keys())
```

### Issue: Context Not Switching

**Symptom**: Stuck in wrong context

**Solution**:
```python
# Check game state
print(bridge.game_state.__dict__)

# Manual switch
bridge.runtime.switch_context('combat')
```

---

## Roadmap

### Phase 1: Core HLVM ✅ **COMPLETE**

**Status**: 100% Complete (November 14, 2025)

- ✅ Global Beat Scheduler (GBS)
- ✅ Track runtime
- ✅ BoolRhythm/TruthValue types
- ✅ Context engine
- ✅ Classical + Fuzzy + **Paraconsistent** ALUs
- ✅ **Paraconsistent logic** (full implementation with contradiction tracking)
- ✅ **Meta-logic operators** (`@coh`, `@conflict`, `@meta`, `@resolve`)
- ✅ **Python FFI** (`python_call()`, `python_execute()`)
- ✅ **Enter context** (dynamic context switching)
- ✅ **Comprehensive test coverage** (all tests passing)

**Implementation**:
- 295 lines paraconsistent logic (`runtime/paraconsistent.py`)
- 368 lines meta-logic (`runtime/metalogic.py`)
- 595 lines test coverage (100% passing)
- Total: 1,431 lines

**See**: `HLVM_PHASE1_COMPLETE.md` for full details

**Phase 1**: ✅ **COMPLETE** - Ready for Phase 2

**Deliverables**:
- Full decorator support for all subsystems
- Automated TruthValue sync protocol
- Beat counter integration with Singularis main loop
- Context switching from game state
- Performance profiling

**Milestones**:
- Week 1: Complete decorator system
- Week 2: Integrate with `skyrim_agi.py` main loop
- Week 3: Port 3-5 subsystems to .haack
- Week 4: Testing and optimization

### Phase 3: Cognitive Module Migration (2-3 months)

**Target Modules**:
1. ✅ `danger_evaluation.haack`
2. ✅ `action_selection.haack`
3. ✅ `coherence_monitoring.haack`
4. ❌ `learning_consolidation.haack`
5. ❌ `meta_orchestration.haack`
6. ❌ `world_model_update.haack`
7. ❌ `combat_tactics.haack`
8. ❌ `exploration_planner.haack`

**Success Criteria**:
- 50%+ of Singularis cognition runs through HaackLang
- No performance regression vs pure Python
- Improved coherence metrics

### Phase 4: Self-Modification (Future)

**Vision**:
- HaackLang programs that modify themselves
- Meta-learning based on coherence
- Automatic track period tuning
- Context emergence from experience

**Research Questions**:
- Can HaackLang modules learn to adjust their own track periods?
- Can new contexts emerge automatically?
- Can meta-logic rules be learned?

---

## Conclusion

HaackLang transforms Singularis from ad-hoc Python coordination to formally guaranteed polyrhythmic cognition. By making temporal rhythms, modal switches, and polylogical truth **first-class citizens**, we move from hoping subsystems synchronize to **knowing** they do.

**This is the score the symphony should be reading from.**

---

**Questions?**  
- See `SINGULARIS_HAACKLANG_INTEGRATION_SPEC.md` for technical specification
- Check `singularis/haacklang_bridge/` for implementation
- Run examples in `singularis/skyrim/Haacklang/examples/`

**Status**: Integration architecture complete ✅  
**Next**: Phase 2 implementation
