"""
Beta v3 Core System Tests

Tests for BeingState and TemporalBinding core systems.
"""

import time
import pytest
from singularis.core.being_state import BeingState, LuminaState
from singularis.core.temporal_binding import TemporalCoherenceTracker


class TestBeingState:
    """Test BeingState - the unified state representation."""
    
    def test_initialization(self):
        """Test BeingState initializes correctly."""
        state = BeingState()
        assert state.cycle_number == 0
        assert state.global_coherence == 0.0
        assert state.temporal_coherence == 0.0
        assert isinstance(state.lumina, LuminaState)
    
    def test_subsystem_update(self):
        """Test subsystem data updates."""
        state = BeingState()
        state.update_subsystem('test_system', {
            'value': 42,
            'status': 'active'
        })
        
        assert state.test_system_value == 42
        assert state.test_system_status == 'active'
        assert state.test_system_timestamp > 0
    
    def test_subsystem_freshness(self):
        """Test subsystem freshness checking."""
        state = BeingState()
        state.update_subsystem('sensorimotor', {'status': 'MOVING'})
        
        # Fresh subsystem
        assert state.is_subsystem_fresh('sensorimotor', max_age=5.0)
        
        # Make it stale
        state.sensorimotor_timestamp = time.time() - 10.0
        assert not state.is_subsystem_fresh('sensorimotor', max_age=5.0)
    
    def test_subsystem_age(self):
        """Test subsystem age calculation."""
        state = BeingState()
        state.update_subsystem('sensorimotor', {'status': 'MOVING'})
        
        age = state.get_subsystem_age('sensorimotor')
        assert age < 1.0  # Should be very recent
        
        # Non-existent subsystem
        age = state.get_subsystem_age('nonexistent')
        assert age == 999.0
    
    def test_subsystem_data_retrieval(self):
        """Test getting all subsystem data."""
        state = BeingState()
        state.update_subsystem('sensorimotor', {
            'status': 'MOVING',
            'analysis': 'Forward movement',
            'visual_similarity': 0.3
        })
        
        data = state.get_subsystem_data('sensorimotor')
        
        assert 'status' in data
        assert 'analysis' in data
        assert 'visual_similarity' in data
        assert 'age' in data
        assert 'is_fresh' in data
        assert data['status'] == 'MOVING'
    
    def test_lumina_balance(self):
        """Test Lumina balance calculation."""
        lumina = LuminaState(ontic=0.8, structural=0.7, participatory=0.9)
        balance = lumina.balance_score()
        assert 0.0 <= balance <= 1.0
        
        # Perfect balance
        lumina_perfect = LuminaState(ontic=0.5, structural=0.5, participatory=0.5)
        assert lumina_perfect.balance_score() > 0.9
    
    def test_export_snapshot(self):
        """Test state snapshot export."""
        state = BeingState()
        state.cycle_number = 42
        state.global_coherence = 0.75
        state.update_subsystem('sensorimotor', {'status': 'MOVING'})
        
        snapshot = state.export_snapshot()
        
        assert 'timestamp' in snapshot
        assert 'cycle' in snapshot
        assert snapshot['cycle'] == 42
        assert 'global_coherence' in snapshot
        assert 'lumina' in snapshot
        assert 'consciousness' in snapshot
        assert 'subsystems' in snapshot
        assert 'sensorimotor' in snapshot['subsystems']


class TestTemporalBinding:
    """Test TemporalCoherenceTracker - temporal binding system."""
    
    def test_initialization(self):
        """Test temporal tracker initializes correctly."""
        tracker = TemporalCoherenceTracker(window_size=20, unclosed_timeout=30.0)
        assert tracker.total_bindings == 0
        assert tracker.unclosed_loops == 0
        assert tracker.successful_loops == 0
    
    def test_bind_perception_to_action(self):
        """Test creating perception-action bindings."""
        tracker = TemporalCoherenceTracker()
        perception = {'visual_similarity': 0.3, 'scene': 'forest'}
        
        binding_id = tracker.bind_perception_to_action(
            perception=perception,
            action='move_forward',
            gemini_visual='Forest path ahead'
        )
        
        assert binding_id is not None
        assert len(binding_id) == 8  # MD5 hash truncated
        assert tracker.total_bindings == 1
        assert tracker.unclosed_loops == 1
    
    def test_close_loop(self):
        """Test closing perception-action loops."""
        tracker = TemporalCoherenceTracker()
        perception = {'visual_similarity': 0.3}
        
        binding_id = tracker.bind_perception_to_action(
            perception=perception,
            action='move_forward'
        )
        
        tracker.close_loop(
            binding_id=binding_id,
            outcome='moved_successfully',
            coherence_delta=0.05,
            success=True
        )
        
        assert tracker.unclosed_loops == 0
        assert tracker.successful_loops == 1
    
    def test_stuck_detection(self):
        """Test stuck loop detection."""
        tracker = TemporalCoherenceTracker()
        
        # Create multiple bindings with high visual similarity
        for i in range(5):
            perception = {'visual_similarity': 0.97}
            tracker.bind_perception_to_action(
                perception=perception,
                action='move_forward'
            )
        
        assert tracker.stuck_loop_count >= 3
        assert tracker.is_stuck()
    
    def test_closure_rate(self):
        """Test closure rate calculation."""
        tracker = TemporalCoherenceTracker()
        
        # Create and close some bindings
        for i in range(10):
            perception = {'visual_similarity': 0.3}
            binding_id = tracker.bind_perception_to_action(
                perception=perception,
                action=f'action_{i}'
            )
            
            if i < 9:  # Close 9 out of 10
                tracker.close_loop(
                    binding_id=binding_id,
                    outcome='success',
                    coherence_delta=0.05,
                    success=True
                )
        
        unclosed_ratio = tracker.get_unclosed_ratio()
        assert 0.0 <= unclosed_ratio <= 0.2  # Should be around 10%
        
        success_rate = tracker.get_success_rate()
        assert success_rate > 0.8
    
    def test_statistics(self):
        """Test getting temporal statistics."""
        tracker = TemporalCoherenceTracker()
        
        # Create some bindings
        for i in range(5):
            perception = {'visual_similarity': 0.3}
            tracker.bind_perception_to_action(
                perception=perception,
                action=f'action_{i}'
            )
        
        stats = tracker.get_statistics()
        
        assert 'total_bindings' in stats
        assert 'unclosed_loops' in stats
        assert 'unclosed_ratio' in stats
        assert 'success_rate' in stats
        assert 'stuck_loop_count' in stats
        assert stats['total_bindings'] == 5


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
