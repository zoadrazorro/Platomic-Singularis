"""
Test Phase 3 Integration - GPT-5 Coordination, Conflict Prevention, and Temporal Binding

Tests Steps 3.3, 3.4, and 3.5 of the emergency stabilization plan.
"""

import asyncio
import time
import pytest
from unittest.mock import Mock, AsyncMock, MagicMock

from singularis.skyrim.action_arbiter import ActionArbiter, ActionPriority
from singularis.core.being_state import BeingState
from singularis.llm.gpt5_orchestrator import GPT5Orchestrator, GPT5Response


# Mock classes
class MockSkyrimAGI:
    """Mock SkyrimAGI for testing."""
    def __init__(self):
        self.current_perception = {
            'game_state': {'health': 100, 'in_combat': False, 'in_menu': False},
            'scene_type': 'exploration',
        }
        self.action_history = []
        self.actions_executed = []
    
    async def _execute_action(self, action, scene_type):
        """Mock action execution."""
        self.actions_executed.append(action)
        self.action_history.append(action)
        await asyncio.sleep(0.05)


class MockTemporalTracker:
    """Mock temporal coherence tracker."""
    def __init__(self, unclosed_ratio=0.1):
        self.unclosed_ratio = unclosed_ratio
    
    def get_statistics(self):
        return {
            'unclosed_ratio': self.unclosed_ratio,
            'total_bindings': 100,
            'unclosed_loops': int(100 * self.unclosed_ratio),
            'success_rate': 0.9
        }


# ═══════════════════════════════════════════════════════════
# STEP 3.3: GPT-5 ORCHESTRATOR COORDINATION
# ═══════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_gpt5_coordination_initialization():
    """Test that arbiter can be initialized with GPT-5 orchestrator."""
    mock_agi = MockSkyrimAGI()
    mock_gpt5 = Mock(spec=GPT5Orchestrator)
    
    arbiter = ActionArbiter(
        skyrim_agi=mock_agi,
        gpt5_orchestrator=mock_gpt5,
        enable_gpt5_coordination=True
    )
    
    assert arbiter.gpt5 == mock_gpt5
    assert arbiter.enable_gpt5_coordination == True
    assert arbiter.gpt5_coordination_count == 0
    
    print("✓ GPT-5 coordination initialization works")


@pytest.mark.asyncio
async def test_coordinate_action_decision():
    """Test GPT-5 action coordination with candidate actions."""
    mock_agi = MockSkyrimAGI()
    
    # Create mock GPT-5 orchestrator
    mock_gpt5 = AsyncMock(spec=GPT5Orchestrator)
    mock_gpt5.send_message = AsyncMock(return_value=GPT5Response(
        response_text="I recommend Action 1 (move_forward) as it has highest confidence and aligns with exploration goals.",
        reasoning="Action 1 has best subsystem consensus",
        confidence=0.85
    ))
    
    arbiter = ActionArbiter(
        skyrim_agi=mock_agi,
        gpt5_orchestrator=mock_gpt5,
        enable_gpt5_coordination=True
    )
    
    # Create BeingState
    being_state = BeingState()
    being_state.cycle_number = 42
    being_state.global_coherence = 0.78
    being_state.temporal_coherence = 0.85
    being_state.unclosed_bindings = 3
    being_state.stuck_loop_count = 0
    being_state.primary_emotion = "curious"
    being_state.emotion_intensity = 0.6
    
    # Update subsystems
    being_state.update_subsystem('sensorimotor', {
        'status': 'MOVING',
        'analysis': 'Forward movement detected',
        'visual_similarity': 0.3
    })
    being_state.update_subsystem('action_plan', {
        'current': 'move_forward',
        'confidence': 0.8,
        'reasoning': 'Exploring new area'
    })
    
    # Candidate actions
    candidate_actions = [
        {'action': 'move_forward', 'priority': 'NORMAL', 'source': 'reasoning', 'confidence': 0.8},
        {'action': 'turn_left', 'priority': 'LOW', 'source': 'exploration', 'confidence': 0.5},
        {'action': 'wait', 'priority': 'LOW', 'source': 'idle', 'confidence': 0.3}
    ]
    
    # Coordinate decision
    selected = await arbiter.coordinate_action_decision(being_state, candidate_actions)
    
    # Verify GPT-5 was called
    assert mock_gpt5.send_message.called
    call_args = mock_gpt5.send_message.call_args
    assert call_args[1]['system_id'] == 'action_arbiter'
    assert call_args[1]['message_type'] == 'action_coordination'
    
    # Verify selection (mock returns action 1)
    assert selected is not None
    assert selected['action'] == 'move_forward'
    assert 'gpt5_reasoning' in selected
    assert 'gpt5_confidence' in selected
    
    # Verify stats
    assert arbiter.gpt5_coordination_count == 1
    assert arbiter.gpt5_coordination_time > 0
    
    print("✓ GPT-5 action coordination works")
    print(f"  Selected: {selected['action']}")
    print(f"  Reasoning: {selected.get('gpt5_reasoning', 'N/A')[:50]}...")


@pytest.mark.asyncio
async def test_coordinate_action_decision_disabled():
    """Test that coordination is skipped when disabled."""
    mock_agi = MockSkyrimAGI()
    
    arbiter = ActionArbiter(
        skyrim_agi=mock_agi,
        gpt5_orchestrator=None,
        enable_gpt5_coordination=False
    )
    
    being_state = BeingState()
    candidate_actions = [{'action': 'move_forward', 'priority': 'NORMAL', 'source': 'test', 'confidence': 0.8}]
    
    selected = await arbiter.coordinate_action_decision(being_state, candidate_actions)
    
    assert selected is None
    assert arbiter.gpt5_coordination_count == 0
    
    print("✓ Coordination correctly skipped when disabled")


# ═══════════════════════════════════════════════════════════
# STEP 3.4: CONFLICT PREVENTION
# ═══════════════════════════════════════════════════════════

def test_conflict_prevention_stuck_loop():
    """Test that stuck loops are detected and prevented."""
    mock_agi = MockSkyrimAGI()
    arbiter = ActionArbiter(mock_agi)
    
    being_state = BeingState()
    being_state.stuck_loop_count = 5  # Stuck!
    
    # Normal action should be blocked
    is_allowed, reason = arbiter.prevent_conflicting_action(
        action='move_forward',
        being_state=being_state,
        priority=ActionPriority.NORMAL
    )
    
    assert is_allowed == False
    assert 'stuck loop' in reason.lower()
    
    # Loop-breaking action should be allowed
    is_allowed, reason = arbiter.prevent_conflicting_action(
        action='turn_left',
        being_state=being_state,
        priority=ActionPriority.NORMAL
    )
    
    assert is_allowed == True
    
    # CRITICAL action should override
    is_allowed, reason = arbiter.prevent_conflicting_action(
        action='move_forward',
        being_state=being_state,
        priority=ActionPriority.CRITICAL
    )
    
    assert is_allowed == True
    
    print("✓ Stuck loop prevention works")


def test_conflict_prevention_temporal_coherence():
    """Test that low temporal coherence triggers conservative behavior."""
    mock_agi = MockSkyrimAGI()
    arbiter = ActionArbiter(mock_agi)
    
    being_state = BeingState()
    being_state.temporal_coherence = 0.3  # Low!
    being_state.unclosed_bindings = 10
    
    # LOW priority should be blocked
    is_allowed, reason = arbiter.prevent_conflicting_action(
        action='explore',
        being_state=being_state,
        priority=ActionPriority.LOW
    )
    
    assert is_allowed == False
    assert 'temporal coherence' in reason.lower()
    
    # NORMAL priority should still work
    is_allowed, reason = arbiter.prevent_conflicting_action(
        action='move_forward',
        being_state=being_state,
        priority=ActionPriority.NORMAL
    )
    
    assert is_allowed == True
    
    print("✓ Temporal coherence check works")


def test_conflict_prevention_subsystem_conflicts():
    """Test detection of subsystem conflicts."""
    mock_agi = MockSkyrimAGI()
    arbiter = ActionArbiter(mock_agi)
    
    being_state = BeingState()
    
    # Sensorimotor says we're stuck
    being_state.update_subsystem('sensorimotor', {
        'status': 'STUCK',
        'analysis': 'No movement detected'
    })
    
    # Action plan recommends something else
    being_state.update_subsystem('action_plan', {
        'current': 'turn_right',
        'confidence': 0.9,
        'reasoning': 'Need to change direction'
    })
    
    # Try to move forward (conflicts with both)
    is_allowed, reason = arbiter.prevent_conflicting_action(
        action='move_forward',
        being_state=being_state,
        priority=ActionPriority.NORMAL
    )
    
    assert is_allowed == False
    assert 'conflict' in reason.lower()
    
    # HIGH priority can override some conflicts
    is_allowed, reason = arbiter.prevent_conflicting_action(
        action='move_forward',
        being_state=being_state,
        priority=ActionPriority.HIGH
    )
    
    # Should be allowed (HIGH can override 1-2 conflicts)
    assert is_allowed == True
    
    print("✓ Subsystem conflict detection works")


def test_conflict_prevention_health_check():
    """Test health-based conflict prevention."""
    mock_agi = MockSkyrimAGI()
    arbiter = ActionArbiter(mock_agi)
    
    being_state = BeingState()
    being_state.game_state = {'health': 15}  # Critical health
    
    # Aggressive action should be blocked
    is_allowed, reason = arbiter.prevent_conflicting_action(
        action='attack',
        being_state=being_state,
        priority=ActionPriority.NORMAL
    )
    
    assert is_allowed == False
    assert 'health' in reason.lower()
    
    # CRITICAL priority should override
    is_allowed, reason = arbiter.prevent_conflicting_action(
        action='attack',
        being_state=being_state,
        priority=ActionPriority.CRITICAL
    )
    
    assert is_allowed == True
    
    print("✓ Health-based conflict prevention works")


# ═══════════════════════════════════════════════════════════
# STEP 3.5: TEMPORAL BINDING CLOSURE
# ═══════════════════════════════════════════════════════════

def test_temporal_binding_closure_excellent():
    """Test closure tracking with excellent closure rate."""
    mock_agi = MockSkyrimAGI()
    arbiter = ActionArbiter(mock_agi)
    
    being_state = BeingState()
    being_state.temporal_coherence = 0.92
    being_state.unclosed_bindings = 2
    being_state.stuck_loop_count = 0
    
    # Mock temporal tracker with good closure
    mock_tracker = MockTemporalTracker(unclosed_ratio=0.03)  # 97% closure
    
    result = arbiter.ensure_temporal_binding_closure(being_state, mock_tracker)
    
    assert result['closure_rate'] >= 0.95
    assert result['status'] == 'EXCELLENT'
    assert result['meets_target'] == True
    assert len(result['recommendations']) == 0
    
    print("✓ Temporal binding closure tracking (excellent) works")
    print(f"  Closure rate: {result['closure_rate']:.1%}")
    print(f"  Status: {result['status']}")


def test_temporal_binding_closure_poor():
    """Test closure tracking with poor closure rate."""
    mock_agi = MockSkyrimAGI()
    arbiter = ActionArbiter(mock_agi)
    
    being_state = BeingState()
    being_state.temporal_coherence = 0.55
    being_state.unclosed_bindings = 15
    being_state.stuck_loop_count = 4
    
    # Mock temporal tracker with poor closure
    mock_tracker = MockTemporalTracker(unclosed_ratio=0.35)  # 65% closure
    
    result = arbiter.ensure_temporal_binding_closure(being_state, mock_tracker)
    
    assert result['closure_rate'] < 0.95
    assert result['status'] in ['FAIR', 'POOR']
    assert result['meets_target'] == False
    assert len(result['recommendations']) > 0
    
    # Check for specific recommendations
    rec_text = ' '.join(result['recommendations']).lower()
    assert 'unclosed bindings' in rec_text or 'stuck loop' in rec_text or 'temporal coherence' in rec_text
    
    print("✓ Temporal binding closure tracking (poor) works")
    print(f"  Closure rate: {result['closure_rate']:.1%}")
    print(f"  Status: {result['status']}")
    print(f"  Recommendations: {len(result['recommendations'])}")
    for i, rec in enumerate(result['recommendations'], 1):
        print(f"    {i}. {rec}")


def test_temporal_binding_closure_stale_subsystems():
    """Test that stale subsystems are detected."""
    mock_agi = MockSkyrimAGI()
    arbiter = ActionArbiter(mock_agi)
    
    being_state = BeingState()
    being_state.temporal_coherence = 0.80
    being_state.unclosed_bindings = 8
    
    # Make subsystems stale
    being_state.update_subsystem('sensorimotor', {'status': 'MOVING'})
    being_state.sensorimotor_timestamp = time.time() - 10.0  # 10 seconds old
    
    being_state.update_subsystem('action_plan', {'current': 'move_forward'})
    being_state.action_plan_timestamp = time.time() - 7.0  # 7 seconds old
    
    result = arbiter.ensure_temporal_binding_closure(being_state, None)
    
    # Should detect stale subsystems
    rec_text = ' '.join(result['recommendations']).lower()
    assert 'stale' in rec_text
    
    print("✓ Stale subsystem detection works")


# ═══════════════════════════════════════════════════════════
# INTEGRATION TEST
# ═══════════════════════════════════════════════════════════

@pytest.mark.asyncio
async def test_phase3_full_integration():
    """Test full Phase 3 integration: coordination + conflict prevention + temporal binding."""
    mock_agi = MockSkyrimAGI()
    
    # Create mock GPT-5
    mock_gpt5 = AsyncMock(spec=GPT5Orchestrator)
    mock_gpt5.send_message = AsyncMock(return_value=GPT5Response(
        response_text="Action 1 recommended",
        reasoning="Best option",
        confidence=0.85
    ))
    
    arbiter = ActionArbiter(
        skyrim_agi=mock_agi,
        gpt5_orchestrator=mock_gpt5,
        enable_gpt5_coordination=True
    )
    
    # Setup BeingState
    being_state = BeingState()
    being_state.cycle_number = 100
    being_state.global_coherence = 0.75
    being_state.temporal_coherence = 0.88
    being_state.unclosed_bindings = 4
    being_state.stuck_loop_count = 0
    
    being_state.update_subsystem('sensorimotor', {'status': 'MOVING', 'visual_similarity': 0.4})
    being_state.update_subsystem('action_plan', {'current': 'explore', 'confidence': 0.7})
    
    # Step 1: GPT-5 coordination
    candidates = [
        {'action': 'explore', 'priority': 'NORMAL', 'source': 'reasoning', 'confidence': 0.7},
        {'action': 'wait', 'priority': 'LOW', 'source': 'idle', 'confidence': 0.3}
    ]
    
    selected = await arbiter.coordinate_action_decision(being_state, candidates)
    assert selected is not None
    
    # Step 2: Conflict prevention
    is_allowed, reason = arbiter.prevent_conflicting_action(
        action=selected['action'],
        being_state=being_state,
        priority=ActionPriority.NORMAL
    )
    assert is_allowed == True
    
    # Step 3: Temporal binding closure check
    mock_tracker = MockTemporalTracker(unclosed_ratio=0.08)  # 92% closure
    closure_result = arbiter.ensure_temporal_binding_closure(being_state, mock_tracker)
    
    # Verify all phases worked
    assert arbiter.gpt5_coordination_count == 1
    assert closure_result['closure_rate'] >= 0.85
    
    print("✓ Full Phase 3 integration works")
    print(f"  GPT-5 coordinations: {arbiter.gpt5_coordination_count}")
    print(f"  Selected action: {selected['action']}")
    print(f"  Conflict check: {reason}")
    print(f"  Closure rate: {closure_result['closure_rate']:.1%}")


def test_phase3_summary():
    """Print Phase 3 completion summary."""
    print("\n" + "="*70)
    print("PHASE 3 COMPLETION SUMMARY")
    print("="*70)
    print("✅ Step 3.3: GPT-5 Orchestrator Coordination")
    print("  - coordinate_action_decision() method added")
    print("  - Gathers subsystem states from BeingState")
    print("  - Queries GPT-5 for coordinated decision")
    print("  - Tracks coordination stats")
    print()
    print("✅ Step 3.4: Conflict Prevention")
    print("  - prevent_conflicting_action() method added")
    print("  - Detects stuck loops, temporal issues, subsystem conflicts")
    print("  - Priority-based override system")
    print("  - Health and state-based validation")
    print()
    print("✅ Step 3.5: Temporal Binding Closure")
    print("  - ensure_temporal_binding_closure() method added")
    print("  - Tracks closure rate (target: >95%)")
    print("  - Provides recommendations for improvement")
    print("  - Detects stale subsystems")
    print()
    print("Features:")
    print("  - GPT-5 meta-cognitive coordination")
    print("  - Multi-level conflict detection")
    print("  - Temporal coherence monitoring")
    print("  - Subsystem consensus checking")
    print("  - Priority-based conflict resolution")
    print()
    print("Expected Results:")
    print("  - Coordinated action decisions across subsystems")
    print("  - Conflict rate: <5%")
    print("  - Temporal binding closure: >95%")
    print("  - Improved action success rate")
    print()
    print("Next Steps:")
    print("  → Phase 4: Full Architecture Test")
    print("  → Run: pytest tests/test_phase3_integration.py -v")
    print("="*70 + "\n")


if __name__ == '__main__':
    """Run tests directly."""
    print("\n" + "="*70)
    print("PHASE 3 TEST SUITE - SUBSYSTEM INTEGRATION")
    print("="*70 + "\n")
    
    # Run synchronous tests
    print("Testing Step 3.4: Conflict Prevention...")
    test_conflict_prevention_stuck_loop()
    test_conflict_prevention_temporal_coherence()
    test_conflict_prevention_subsystem_conflicts()
    test_conflict_prevention_health_check()
    
    print("\nTesting Step 3.5: Temporal Binding Closure...")
    test_temporal_binding_closure_excellent()
    test_temporal_binding_closure_poor()
    test_temporal_binding_closure_stale_subsystems()
    
    # Run async tests
    print("\nTesting Step 3.3: GPT-5 Coordination...")
    asyncio.run(test_gpt5_coordination_initialization())
    asyncio.run(test_coordinate_action_decision())
    asyncio.run(test_coordinate_action_decision_disabled())
    
    print("\nTesting Full Integration...")
    asyncio.run(test_phase3_full_integration())
    
    # Print summary
    test_phase3_summary()
    
    print("\n✅ ALL PHASE 3 TESTS PASSED\n")
