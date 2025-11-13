"""
Adaptive Hierarchical Memory with Forgetting

Extends hierarchical memory with adaptive forgetting to prevent:
1. Overfitting to early experiences
2. Stale patterns dominating new contexts
3. Memory bloat over long sessions

Key Innovation: Patterns decay when unused but strengthen when accessed.
This creates dynamic, context-adaptive memory.
"""

import time
import asyncio
from collections import defaultdict
from typing import Dict, Any, Optional
from loguru import logger

from .hierarchical_memory import HierarchicalMemory, SemanticPattern


class AdaptiveHierarchicalMemory(HierarchicalMemory):
    """
    Hierarchical memory with adaptive forgetting.
    
    Patterns decay over time when unused, but strengthen when accessed.
    This prevents overfitting and enables context-adaptive learning.
    """
    
    def __init__(
        self,
        *args,
        decay_rate: float = 0.95,
        access_boost: float = 1.02,
        forget_threshold: float = 0.1,
        **kwargs
    ):
        """
        Initialize adaptive memory.
        
        Args:
            decay_rate: Per-consolidation confidence decay (0-1)
            access_boost: Confidence boost on successful retrieval
            forget_threshold: Confidence below which patterns are forgotten
            *args, **kwargs: Passed to parent HierarchicalMemory
        """
        super().__init__(*args, **kwargs)
        
        self.decay_rate = decay_rate
        self.access_boost = access_boost
        self.forget_threshold = forget_threshold
        
        # Track pattern access
        self.pattern_last_accessed: Dict[str, float] = {}
        self.pattern_access_count: Dict[str, int] = defaultdict(int)
        
        # Track forgotten patterns
        self.patterns_forgotten = 0
        
        logger.info(
            f"[MEMORY] Adaptive memory initialized "
            f"(decay={decay_rate}, boost={access_boost}, threshold={forget_threshold})"
        )
    
    async def _consolidate(self):
        """Consolidate with confidence decay for unused patterns."""
        # Run parent consolidation
        await super()._consolidate()
        
        # Apply decay to unused patterns
        now = time.time()
        patterns_to_forget = []
        
        for pattern_key, pattern in list(self.semantic.items()):
            # Get last access time
            last_access = self.pattern_last_accessed.get(pattern_key, now)
            time_since_access = now - last_access
            
            # Decay confidence based on time unused
            if time_since_access > 300:  # 5 minutes unused
                access_count = self.pattern_access_count.get(pattern_key, 0)
                
                # Calculate decay
                decay_factor = self.decay_rate ** (time_since_access / 60)
                
                # Stronger decay if never used (newly consolidated)
                if access_count == 0:
                    decay_factor *= 0.8
                
                # Apply decay
                old_confidence = pattern.confidence
                pattern.confidence *= decay_factor
                
                logger.debug(
                    f"[MEMORY] Decaying {pattern_key}: "
                    f"{old_confidence:.3f} → {pattern.confidence:.3f} "
                    f"(unused for {time_since_access/60:.1f}min)"
                )
                
                # Mark for forgetting if too low
                if pattern.confidence < self.forget_threshold:
                    patterns_to_forget.append(pattern_key)
        
        # Forget low-confidence patterns
        for pattern_key in patterns_to_forget:
            pattern = self.semantic[pattern_key]
            logger.info(
                f"[MEMORY] Forgetting pattern {pattern_key}: {pattern.optimal_action} "
                f"(confidence={pattern.confidence:.3f}, "
                f"accessed={self.pattern_access_count.get(pattern_key, 0)}x)"
            )
            
            del self.semantic[pattern_key]
            
            if pattern_key in self.pattern_last_accessed:
                del self.pattern_last_accessed[pattern_key]
            if pattern_key in self.pattern_access_count:
                del self.pattern_access_count[pattern_key]
            
            self.patterns_forgotten += 1
    
    def retrieve_semantic(
        self,
        scene_type: str,
        min_confidence: float = 0.3
    ) -> Optional[SemanticPattern]:
        """
        Retrieve semantic pattern with access tracking.
        
        Accessed patterns get confidence boost and access tracking.
        
        Args:
            scene_type: Type of scene
            min_confidence: Minimum confidence threshold
            
        Returns:
            Semantic pattern or None
        """
        pattern = super().retrieve_semantic(scene_type, min_confidence)
        
        if pattern:
            pattern_key = f"{scene_type}_optimal_action"
            
            # Update access tracking
            self.pattern_last_accessed[pattern_key] = time.time()
            self.pattern_access_count[pattern_key] += 1
            
            # Boost confidence on successful retrieval
            old_confidence = pattern.confidence
            pattern.confidence = min(1.0, pattern.confidence * self.access_boost)
            
            logger.debug(
                f"[MEMORY] Retrieved {pattern_key}: {pattern.optimal_action} "
                f"(confidence={old_confidence:.3f}→{pattern.confidence:.3f}, "
                f"accessed={self.pattern_access_count[pattern_key]}x)"
            )
        
        return pattern
    
    def reinforce_pattern(
        self,
        scene_type: str,
        action: str,
        success: bool
    ):
        """
        Reinforce or weaken pattern based on outcome.
        
        Args:
            scene_type: Type of scene
            action: Action taken
            success: Whether action was successful
        """
        pattern_key = f"{scene_type}_optimal_action"
        
        if pattern_key not in self.semantic:
            # Create new pattern
            pattern = SemanticPattern(
                pattern_key=pattern_key,
                scene_type=scene_type,
                optimal_action=action,
                success_rate=1.0 if success else 0.0,
                sample_size=1,
                confidence=0.5,
                first_learned=time.time(),
                last_updated=time.time(),
                contexts=[]
            )
            
            self.semantic[pattern_key] = pattern
            self.pattern_last_accessed[pattern_key] = time.time()
            
            logger.info(
                f"[MEMORY] Created pattern {pattern_key}: {action} "
                f"(success={success})"
            )
        else:
            pattern = self.semantic[pattern_key]
            
            if pattern.optimal_action == action:
                # Reinforce existing pattern
                if success:
                    old_confidence = pattern.confidence
                    pattern.confidence = min(1.0, pattern.confidence * 1.1)
                    logger.info(
                        f"[MEMORY] Reinforced {pattern_key}: {action} "
                        f"({old_confidence:.3f}→{pattern.confidence:.3f})"
                    )
                else:
                    old_confidence = pattern.confidence
                    pattern.confidence *= 0.9
                    logger.warning(
                        f"[MEMORY] Weakened {pattern_key}: {action} "
                        f"({old_confidence:.3f}→{pattern.confidence:.3f})"
                    )
            else:
                # Contradictory evidence
                old_confidence = pattern.confidence
                pattern.confidence *= 0.85
                
                logger.warning(
                    f"[MEMORY] Contradictory evidence for {pattern_key}: "
                    f"expected {pattern.optimal_action}, got {action} "
                    f"(confidence {old_confidence:.3f}→{pattern.confidence:.3f})"
                )
                
                # Replace if confidence drops too low
                if pattern.confidence < 0.3:
                    logger.info(
                        f"[MEMORY] Replacing {pattern_key}: "
                        f"{pattern.optimal_action} → {action}"
                    )
                    pattern.optimal_action = action
                    pattern.confidence = 0.5
                    pattern.success_rate = 1.0 if success else 0.0
                    pattern.sample_size = 1
            
            # Update metadata
            pattern.last_updated = time.time()
            self.pattern_last_accessed[pattern_key] = time.time()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get adaptive memory statistics."""
        stats = super().get_statistics()
        
        # Add adaptive-specific stats
        stats['patterns_forgotten'] = self.patterns_forgotten
        stats['avg_access_count'] = (
            sum(self.pattern_access_count.values()) / len(self.pattern_access_count)
            if self.pattern_access_count else 0.0
        )
        stats['total_accesses'] = sum(self.pattern_access_count.values())
        
        return stats
