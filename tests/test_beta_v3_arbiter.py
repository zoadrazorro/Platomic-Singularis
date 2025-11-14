"""
Beta v3 ActionArbiter Tests

Tests for ActionArbiter including Phase 2 and Phase 3 features.
"""

import asyncio
import time
import pytest
from unittest.mock import AsyncMock

from singularis.skyrim.action_arbiter import ActionArbiter, ActionPriority
from singularis.core.being_state import BeingState
from singularis.llm.gpt5_orchestrator import GPT5Orchestrator, GPT5Response


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
        self.actions_executed.append(action)
        self.action_history.append(action)
        await asyncio.sleep(0.05)


class TestActionArbiterBasics:
    """Test basic ActionArbiter functionality (Phase 2)."""
    
    def test_initialization(self):
        """Test arbiter initializes correctly."""
        mock_agi = MockSkyrimAGI()
        arbiter = ActionArbiter(mock_agi)
        
        assert arbiter.action_executing == False
        assert arbiter.stats['total_requests'] == 0
        assert arbiter.stats['executed'] == 0
    
    @pytest.mark.asyncio
    async def test_basic_action_request(self):
        """Test basic action request and execution."""
        mock_agi = MockSkyrimAGI()
        arbiter = ActionArbiter(mock_agi)
        
        result = await arbiter.request_action(
            action='move_forward',
            priority=ActionPriority.NORMAL,
            source='test',
            context={
                'perception_timestamp': time.time(),
                'scene_type': 'exploration',
                'game_state': {'health': 100}
            }
        )
        
        assert result.executed == True
        assert result.success == True
        assert arbiter.stats['total_requests'] == 1
        assert arbiter.stats['executed'] == 1
    
    @pytest.mark.asyncio
    async def test_stale_perception_rejection(self):
        """Test that stale perceptions are rejected."""
        mock_agi = MockSkyrimAGI()
        arbiter = ActionArbiter(mock_agi)
        
        result = await arbiter.request_action(
            action='move_forward',
            priority=ActionPriority.NORMAL,
            source='test',
            context={
                'perception_timestamp': time.time() - 5.0,  # 5 seconds old
                'scene_type': 'exploration',
                'game_state': {'health': 100}
            }
        )
        
        assert result.executed == False
        assert 'too old' in result.reason.lower()
        assert arbiter.stats['rejected'] == 1
    
    @pytest.mark.asyncio
    async def test_priority_system(self):
        """Test priority levels work correctly."""
        mock_agi = MockSkyrimAGI()
        arbiter = ActionArbiter(mock_agi)
        
        # Test all priority levels
        for priority in [ActionPriority.LOW, ActionPriority.NORMAL, 
                        ActionPriority.HIGH, ActionPriority.CRITICAL]:
            result = await arbiter.request_action(
                action=f'action_{priority.name}',
                priority=priority,
                source='test',
                context={
                    'perception_timestamp': time.time(),
                    'scene_type': 'exploration',
                    'game_state': {'health': 100}
                }
            )
            assert result.executed == True
        
        assert arbiter.stats['total_requests'] == 4


class TestConflictPrevention:
    """Test conflict prevention (Phase 3.4)."""
    
    def test_stuck_loop_prevention(self):
        """Test stuck loop detection and prevention."""
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
    
    def test_temporal_coherence_check(self):
        """Test temporal coherence-based prevention."""
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
    
    def test_subsystem_conflicts(self):
        """Test subsystem conflict detection."""
        mock_agi = MockSkyrimAGI()
        arbiter = ActionArbiter(mock_agi)
        
        being_state = BeingState()
        
        # Sensorimotor says we're stuck
        being_state.update_subsystem('sensorimotor', {
            'status': 'STUCK',
            'analysis': 'No movement detected'
        })
        
        # Try to move forward (conflicts with stuck status)
        is_allowed, reason = arbiter.prevent_conflicting_action(
            action='move_forward',
            being_state=being_state,
            priority=ActionPriority.NORMAL
        )
        
        assert is_allowed == False
        assert 'conflict' in reason.lower()
    
    def test_health_based_conflicts(self):
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


class TestTemporalBindingClosure:
    """Test temporal binding closure tracking (Phase 3.5)."""
    
    def test_excellent_closure(self):
        """Test tracking with excellent closure rate."""
        mock_agi = MockSkyrimAGI()
        arbiter = ActionArbiter(mock_agi)
        
        being_state = BeingState()
        being_state.temporal_coherence = 0.92
        being_state.unclosed_bindings = 2
        being_state.stuck_loop_count = 0
        
        result = arbiter.ensure_temporal_binding_closure(being_state, None)
        
        assert result['closure_rate'] >= 0.95
        assert result['status'] == 'EXCELLENT'
        assert result['meets_target'] == True
        assert len(result['recommendations']) == 0
    
    def test_poor_closure(self):
        """Test tracking with poor closure rate."""
        mock_agi = MockSkyrimAGI()
        arbiter = ActionArbiter(mock_agi)
        
        being_state = BeingState()
        being_state.temporal_coherence = 0.55
        being_state.unclosed_bindings = 15
        being_state.stuck_loop_count = 4
        
        result = arbiter.ensure_temporal_binding_closure(being_state, None)
        
        assert result['closure_rate'] < 0.95
        assert result['status'] in ['FAIR', 'POOR']
        assert result['meets_target'] == False
        assert len(result['recommendations']) > 0
    
    def test_stale_subsystem_detection(self):
        """Test detection of stale subsystems."""
        mock_agi = MockSkyrimAGI()
        arbiter = ActionArbiter(mock_agi)
        
        being_state = BeingState()
        being_state.temporal_coherence = 0.80
        being_state.unclosed_bindings = 8
        
        # Make subsystems stale
        being_state.update_subsystem('sensorimotor', {'status': 'MOVING'})
        being_state.sensorimotor_timestamp = time.time() - 10.0
        
        result = arbiter.ensure_temporal_binding_closure(being_state, None)
        
        # Should detect stale subsystems
        rec_text = ' '.join(result['recommendations']).lower()
        assert 'stale' in rec_text


class TestGPT5Coordination:
    """Test GPT-5 coordination (Phase 3.3)."""
    
    @pytest.mark.asyncio
    async def test_coordinate_action_decision(self):
        """Test GPT-5 action coordination."""
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
        
        being_state = BeingState()
        being_state.cycle_number = 42
        being_state.global_coherence = 0.75
        being_state.update_subsystem('sensorimotor', {'status': 'MOVING'})
        
        candidate_actions = [
            {'action': 'move_forward', 'priority': 'NORMAL', 'source': 'reasoning', 'confidence': 0.8},
            {'action': 'turn_left', 'priority': 'LOW', 'source': 'exploration', 'confidence': 0.5}
        ]
        
        selected = await arbiter.coordinate_action_decision(being_state, candidate_actions)
        
        # Verify GPT-5 was called
        assert mock_gpt5.send_message.called
        assert arbiter.gpt5_coordination_count == 1
        
        # Verify selection
        assert selected is not None
        assert 'gpt5_reasoning' in selected or selected['action'] in ['move_forward', 'turn_left']
    
    @pytest.mark.asyncio
    async def test_coordination_disabled(self):
        """Test that coordination is skipped when disabled."""
        mock_agi = MockSkyrimAGI()
        arbiter = ActionArbiter(
            skyrim_agi=mock_agi,
            gpt5_orchestrator=None,
            enable_gpt5_coordination=False
        )
        
        being_state = BeingState()
        candidate_actions = [
            {'action': 'move_forward', 'priority': 'NORMAL', 'source': 'test', 'confidence': 0.8}
        ]
        
        selected = await arbiter.coordinate_action_decision(being_state, candidate_actions)
        
        assert selected is None
        assert arbiter.gpt5_coordination_count == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
