"""
Lumen-Responsive Orchestrator

Actively balances Lumen (Onticum/Structurale/Participatum) by adjusting
subsystem activation based on detected imbalances.

Key Innovation: Philosophical insights become active corrections, not passive
observations. The system maintains holistic balance through dynamic rebalancing.
"""

import asyncio
from collections import deque, defaultdict
from typing import Dict, Any, Optional, Set
from loguru import logger

from .lumen_integration import LumenIntegratedSystem, LumenBalance


class LumenBalancedOrchestrator:
    """
    Orchestrator that actively balances Lumen aspects.
    
    Detects imbalances and triggers subsystem activation to restore
    holistic expression of Being across Onticum/Structurale/Participatum.
    """
    
    def __init__(
        self,
        lumen_integration: LumenIntegratedSystem,
        severe_threshold: float = 0.5,
        moderate_threshold: float = 0.7
    ):
        """
        Initialize Lumen-balanced orchestrator.
        
        Args:
            lumen_integration: Lumen integration system
            severe_threshold: Balance score below which emergency rebalancing triggers
            moderate_threshold: Balance score below which gradual rebalancing triggers
        """
        self.lumen = lumen_integration
        
        # Subsystem activation weights
        self.activation_weights: Dict[str, float] = defaultdict(lambda: 1.0)
        
        # Balance history
        self.balance_history: deque[LumenBalance] = deque(maxlen=50)
        
        # Thresholds
        self.severe_imbalance_threshold = severe_threshold
        self.moderate_imbalance_threshold = moderate_threshold
        
        # Rebalancing stats
        self.total_rebalances = 0
        self.emergency_rebalances = 0
        self.gradual_rebalances = 0
        
        logger.info(
            f"[LUMEN-ORCH] Initialized "
            f"(severe<{severe_threshold}, moderate<{moderate_threshold})"
        )
    
    async def rebalance_subsystems(
        self,
        current_balance: LumenBalance,
        available_subsystems: Dict[str, Any]
    ):
        """
        Actively rebalance Lumen by adjusting subsystem activation.
        
        Args:
            current_balance: Current Lumen balance
            available_subsystems: Available subsystems for activation
        """
        # Track balance
        self.balance_history.append(current_balance)
        
        if current_balance.balance_score < self.severe_imbalance_threshold:
            logger.warning(
                f"[LUMEN-ORCH] SEVERE IMBALANCE: {current_balance.imbalance_direction} "
                f"(score={current_balance.balance_score:.3f})"
            )
            
            # Emergency rebalancing
            await self._emergency_rebalance(current_balance, available_subsystems)
            self.emergency_rebalances += 1
            
        elif current_balance.balance_score < self.moderate_imbalance_threshold:
            logger.info(
                f"[LUMEN-ORCH] Moderate imbalance: {current_balance.imbalance_direction} "
                f"(score={current_balance.balance_score:.3f})"
            )
            
            # Gradual rebalancing
            await self._gradual_rebalance(current_balance, available_subsystems)
            self.gradual_rebalances += 1
        
        self.total_rebalances += 1
    
    async def _emergency_rebalance(
        self,
        balance: LumenBalance,
        subsystems: Dict[str, Any]
    ):
        """
        Emergency rebalancing - force activation of deficient Lumen.
        
        Args:
            balance: Current Lumen balance
            subsystems: Available subsystems
        """
        direction = balance.imbalance_direction
        
        if "onticum" in direction and "deficit" in direction:
            # Activate energy/motivation systems
            logger.info("[LUMEN-ORCH] Activating Onticum systems (emotion, motivation)")
            
            tasks = []
            
            # Force emotion system query
            if 'emotion' in subsystems and hasattr(subsystems['emotion'], 'process_emergency'):
                tasks.append(subsystems['emotion'].process_emergency())
            
            # Force motivation spike
            if 'motivation' in subsystems and hasattr(subsystems['motivation'], 'boost_curiosity'):
                tasks.append(subsystems['motivation'].boost_curiosity())
            
            # Activate spiritual awareness
            if 'spiritual' in subsystems and hasattr(subsystems['spiritual'], 'emergency_contemplation'):
                tasks.append(subsystems['spiritual'].emergency_contemplation())
            
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
        
        elif "structurale" in direction and "deficit" in direction:
            # Activate logic/structure systems
            logger.info("[LUMEN-ORCH] Activating Structurale systems (logic, world_model)")
            
            tasks = []
            
            # Force logic verification
            if 'symbolic_logic' in subsystems and hasattr(subsystems['symbolic_logic'], 'verify_current_state'):
                tasks.append(subsystems['symbolic_logic'].verify_current_state())
            
            # Update world model
            if 'world_model' in subsystems and hasattr(subsystems['world_model'], 'rebuild_causal_graph'):
                tasks.append(subsystems['world_model'].rebuild_causal_graph())
            
            # Activate perception
            if 'perception' in subsystems and hasattr(subsystems['perception'], 'deep_analysis'):
                tasks.append(subsystems['perception'].deep_analysis())
            
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
        
        elif "participatum" in direction and "deficit" in direction:
            # Activate consciousness/awareness systems
            logger.info("[LUMEN-ORCH] Activating Participatum systems (consciousness, reflection)")
            
            tasks = []
            
            # Force self-reflection
            if 'self_reflection' in subsystems and hasattr(subsystems['self_reflection'], 'reflect_on_current_state'):
                tasks.append(subsystems['self_reflection'].reflect_on_current_state())
            
            # Consciousness bridge integration
            if 'consciousness_bridge' in subsystems and hasattr(subsystems['consciousness_bridge'], 'measure_coherence'):
                tasks.append(subsystems['consciousness_bridge'].measure_coherence())
            
            # Meta-strategic awareness
            if 'meta_strategist' in subsystems and hasattr(subsystems['meta_strategist'], 'strategic_reflection'):
                tasks.append(subsystems['meta_strategist'].strategic_reflection())
            
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _gradual_rebalance(
        self,
        balance: LumenBalance,
        subsystems: Dict[str, Any]
    ):
        """
        Gradual rebalancing - adjust activation weights.
        
        Args:
            balance: Current Lumen balance
            subsystems: Available subsystems
        """
        # Identify deficient Lumen
        lumen_levels = {
            'onticum': balance.onticum,
            'structurale': balance.structurale,
            'participatum': balance.participatum
        }
        
        min_lumen = min(lumen_levels, key=lumen_levels.get)
        min_activity = lumen_levels[min_lumen]
        
        # Compute boost factor (inverse proportion)
        boost_factor = 1.2 / (min_activity + 0.1)
        boost_factor = min(2.0, boost_factor)  # Cap at 2x
        
        # Get systems to boost
        if min_lumen == 'onticum':
            systems_to_boost = self.lumen.onticum_systems
        elif min_lumen == 'structurale':
            systems_to_boost = self.lumen.structurale_systems
        else:
            systems_to_boost = self.lumen.participatum_systems
        
        # Boost deficient systems
        boosted_count = 0
        for system in systems_to_boost:
            if system in subsystems:
                old_weight = self.activation_weights[system]
                self.activation_weights[system] = min(2.0, old_weight * boost_factor)
                
                logger.debug(
                    f"[LUMEN-ORCH] Boosting {system}: "
                    f"{old_weight:.2f} → {self.activation_weights[system]:.2f}"
                )
                boosted_count += 1
        
        logger.info(
            f"[LUMEN-ORCH] Boosted {boosted_count} {min_lumen} systems "
            f"(factor={boost_factor:.2f})"
        )
    
    def get_activation_weight(self, system_id: str) -> float:
        """Get current activation weight for system."""
        return self.activation_weights[system_id]
    
    def reset_weights(self):
        """Reset all activation weights to 1.0."""
        self.activation_weights.clear()
        logger.info("[LUMEN-ORCH] Reset all activation weights")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get Lumen orchestrator statistics."""
        return {
            'total_rebalances': self.total_rebalances,
            'emergency_rebalances': self.emergency_rebalances,
            'gradual_rebalances': self.gradual_rebalances,
            'balance_history_size': len(self.balance_history),
            'avg_balance_score': (
                sum(b.balance_score for b in self.balance_history) / len(self.balance_history)
                if self.balance_history else 0.0
            ),
            'current_weights': dict(self.activation_weights),
        }
