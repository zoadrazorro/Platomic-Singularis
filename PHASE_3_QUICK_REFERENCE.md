# Phase 3 Quick Reference Guide

## Usage Examples

### 1. Initialize ActionArbiter with GPT-5 Coordination

```python
from singularis.skyrim.action_arbiter import ActionArbiter, ActionPriority
from singularis.llm.gpt5_orchestrator import GPT5Orchestrator
from singularis.core.being_state import BeingState

# Initialize GPT-5 orchestrator
gpt5 = GPT5Orchestrator(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-5",
    verbose=True
)

# Register action arbiter
gpt5.register_system("action_arbiter", SystemType.ACTION)

# Initialize arbiter with GPT-5
arbiter = ActionArbiter(
    skyrim_agi=agi,
    gpt5_orchestrator=gpt5,
    enable_gpt5_coordination=True
)
```

### 2. Coordinate Action Decision (Step 3.3)

```python
# Prepare candidate actions
candidate_actions = [
    {
        'action': 'move_forward',
        'priority': 'NORMAL',
        'source': 'reasoning_loop',
        'confidence': 0.8
    },
    {
        'action': 'turn_left',
        'priority': 'LOW',
        'source': 'exploration',
        'confidence': 0.5
    },
    {
        'action': 'heal',
        'priority': 'HIGH',
        'source': 'survival',
        'confidence': 0.9
    }
]

# Coordinate through GPT-5
selected_action = await arbiter.coordinate_action_decision(
    being_state=being_state,
    candidate_actions=candidate_actions
)

if selected_action:
    print(f"GPT-5 selected: {selected_action['action']}")
    print(f"Reasoning: {selected_action['gpt5_reasoning']}")
    print(f"Confidence: {selected_action['gpt5_confidence']:.2f}")
```

### 3. Prevent Conflicting Actions (Step 3.4)

```python
# Check for conflicts before execution
is_allowed, reason = arbiter.prevent_conflicting_action(
    action='move_forward',
    being_state=being_state,
    priority=ActionPriority.NORMAL
)

if is_allowed:
    # Execute action
    await arbiter.request_action(
        action='move_forward',
        priority=ActionPriority.NORMAL,
        source='main_loop',
        context={
            'perception_timestamp': time.time(),
            'scene_type': 'exploration',
            'game_state': game_state
        }
    )
else:
    print(f"Action blocked: {reason}")
```

### 4. Ensure Temporal Binding Closure (Step 3.5)

```python
# Check temporal binding closure
closure_result = arbiter.ensure_temporal_binding_closure(
    being_state=being_state,
    temporal_tracker=temporal_tracker  # Optional
)

print(f"Closure rate: {closure_result['closure_rate']:.1%}")
print(f"Status: {closure_result['status']}")
print(f"Meets target (>95%): {closure_result['meets_target']}")

if not closure_result['meets_target']:
    print("\nRecommendations:")
    for rec in closure_result['recommendations']:
        print(f"  - {rec}")
```

### 5. Complete Integration Example

```python
async def main_action_loop(agi, arbiter, being_state, temporal_tracker):
    """Complete action loop with Phase 3 integration."""
    
    # Step 1: Gather candidate actions from subsystems
    candidate_actions = []
    
    # From reasoning loop
    if being_state.is_subsystem_fresh('action_plan'):
        action_data = being_state.get_subsystem_data('action_plan')
        candidate_actions.append({
            'action': action_data['current'],
            'priority': 'NORMAL',
            'source': 'reasoning',
            'confidence': action_data['confidence']
        })
    
    # From memory recommendations
    if being_state.is_subsystem_fresh('memory'):
        memory_data = being_state.get_subsystem_data('memory')
        for rec in memory_data.get('recommendations', [])[:2]:
            candidate_actions.append({
                'action': rec,
                'priority': 'LOW',
                'source': 'memory',
                'confidence': 0.6
            })
    
    # From emotion system
    if being_state.is_subsystem_fresh('emotion'):
        emotion_data = being_state.get_subsystem_data('emotion')
        for rec in emotion_data.get('recommendations', [])[:1]:
            candidate_actions.append({
                'action': rec,
                'priority': 'HIGH' if being_state.emotion_intensity > 0.8 else 'NORMAL',
                'source': 'emotion',
                'confidence': being_state.emotion_intensity
            })
    
    # Step 2: GPT-5 coordination (if enabled)
    selected = None
    if arbiter.enable_gpt5_coordination and len(candidate_actions) > 1:
        selected = await arbiter.coordinate_action_decision(
            being_state=being_state,
            candidate_actions=candidate_actions
        )
    else:
        # Fallback: select highest confidence
        selected = max(candidate_actions, key=lambda x: x['confidence'])
    
    if not selected:
        return
    
    # Step 3: Conflict prevention
    priority = ActionPriority[selected['priority']]
    is_allowed, reason = arbiter.prevent_conflicting_action(
        action=selected['action'],
        being_state=being_state,
        priority=priority
    )
    
    if not is_allowed:
        logger.warning(f"Action blocked: {reason}")
        return
    
    # Step 4: Execute action
    result = await arbiter.request_action(
        action=selected['action'],
        priority=priority,
        source=selected['source'],
        context={
            'perception_timestamp': time.time(),
            'scene_type': being_state.current_perception.get('scene_type', 'unknown'),
            'game_state': being_state.game_state
        }
    )
    
    # Step 5: Check temporal binding closure
    closure_result = arbiter.ensure_temporal_binding_closure(
        being_state=being_state,
        temporal_tracker=temporal_tracker
    )
    
    if not closure_result['meets_target']:
        logger.warning(
            f"Temporal binding closure below target: {closure_result['closure_rate']:.1%}"
        )
    
    return result
```

## BeingState Integration

### Update Subsystem Data

```python
# Sensorimotor subsystem
being_state.update_subsystem('sensorimotor', {
    'status': 'MOVING',
    'analysis': 'Forward movement detected',
    'visual_similarity': 0.35
})

# Action planning subsystem
being_state.update_subsystem('action_plan', {
    'current': 'explore',
    'confidence': 0.75,
    'reasoning': 'New area detected'
})

# Memory subsystem
being_state.update_subsystem('memory', {
    'pattern_count': 12,
    'similar_situations': similar_situations,
    'recommendations': ['move_forward', 'turn_right']
})

# Emotion subsystem
being_state.update_subsystem('emotion', {
    'recommendations': ['explore', 'investigate']
})
```

### Check Subsystem Freshness

```python
# Check if data is fresh (<5 seconds old)
if being_state.is_subsystem_fresh('sensorimotor', max_age=5.0):
    data = being_state.get_subsystem_data('sensorimotor')
    print(f"Status: {data['status']}")
    print(f"Age: {data['age']:.1f}s")
else:
    print("Sensorimotor data is stale")
```

## Testing

### Run All Phase 3 Tests

```bash
# Run all tests
pytest tests/test_phase3_integration.py -v

# Run specific test
pytest tests/test_phase3_integration.py::test_coordinate_action_decision -v

# Run with output
pytest tests/test_phase3_integration.py -v -s

# Run directly
python tests/test_phase3_integration.py
```

### Expected Output

```
✓ GPT-5 coordination initialization works
✓ GPT-5 action coordination works
✓ Coordination correctly skipped when disabled
✓ Stuck loop prevention works
✓ Temporal coherence check works
✓ Subsystem conflict detection works
✓ Health-based conflict prevention works
✓ Temporal binding closure tracking (excellent) works
✓ Temporal binding closure tracking (poor) works
✓ Stale subsystem detection works
✓ Full Phase 3 integration works

✅ ALL PHASE 3 TESTS PASSED
```

## Monitoring

### Print Arbiter Statistics

```python
# Get statistics
stats = arbiter.get_stats()

print(f"Total requests: {stats['total_requests']}")
print(f"Executed: {stats['executed']}")
print(f"Rejected: {stats['rejected']}")
print(f"Rejection rate: {stats['rejection_rate']:.1%}")
print(f"Override rate: {stats['override_rate']:.1%}")

if arbiter.enable_gpt5_coordination:
    print(f"\nGPT-5 Coordinations: {arbiter.gpt5_coordination_count}")
    if arbiter.gpt5_coordination_count > 0:
        avg_time = arbiter.gpt5_coordination_time / arbiter.gpt5_coordination_count
        print(f"Avg coordination time: {avg_time:.2f}s")

# Or use formatted output
arbiter.print_stats()
```

## Troubleshooting

### GPT-5 Coordination Not Working

```python
# Check if GPT-5 is enabled
if not arbiter.enable_gpt5_coordination:
    print("GPT-5 coordination is disabled")
    
# Check if GPT-5 orchestrator is set
if arbiter.gpt5 is None:
    print("GPT-5 orchestrator not initialized")
    
# Check API key
if not arbiter.gpt5.api_key:
    print("OpenAI API key not configured")
```

### High Conflict Rate

```python
# Check conflict reasons
stats = arbiter.get_stats()
print("Top rejection reasons:")
for reason, count in stats['rejection_reasons'].items():
    print(f"  {reason}: {count}")

# Common fixes:
# 1. Reduce stuck_loop_count threshold
# 2. Improve temporal coherence
# 3. Update subsystem data more frequently
# 4. Use higher priority for important actions
```

### Low Temporal Binding Closure

```python
closure_result = arbiter.ensure_temporal_binding_closure(
    being_state=being_state,
    temporal_tracker=temporal_tracker
)

if not closure_result['meets_target']:
    print(f"Closure rate: {closure_result['closure_rate']:.1%}")
    print(f"Unclosed bindings: {closure_result['unclosed_bindings']}")
    
    # Apply recommendations
    for rec in closure_result['recommendations']:
        print(f"  - {rec}")
    
    # Common fixes:
    # 1. Increase action execution frequency
    # 2. Reduce cycle interval
    # 3. Update subsystems more frequently
    # 4. Force loop-breaking actions when stuck
```

## Performance Targets

| Metric | Target | Typical | Excellent |
|--------|--------|---------|-----------|
| GPT-5 coordination time | <2.0s | 0.5-1.5s | <0.5s |
| Conflict detection rate | >95% | 95-98% | >98% |
| False positive rate | <5% | 2-5% | <2% |
| Temporal binding closure | >95% | 85-97% | >97% |
| Unclosed bindings | <10 | 3-8 | <5 |
| Subsystem consensus | >80% | 80-90% | >90% |

## Next Steps

1. **Integrate with SkyrimAGI**: Wire up ActionArbiter in main loop
2. **Connect TemporalTracker**: Pass tracker to closure method
3. **Enable GPT-5**: Set up orchestrator and API key
4. **Run Phase 4 Tests**: Measure end-to-end performance
5. **24-hour Stability**: Monitor long-running operation

## Documentation

- **Full Documentation**: `PHASE_3_COMPLETE.md`
- **Test Suite**: `tests/test_phase3_integration.py`
- **Main Tracking**: `PHASE_1_EMERGENCY_STABILIZATION.md`
- **This Guide**: `PHASE_3_QUICK_REFERENCE.md`
