"""
LLM Response Caching System for Singularis.

Caches common scene→action patterns to reduce redundant LLM queries.
Uses TTL-based expiration and similarity matching for intelligent retrieval.
"""

import hashlib
import time
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import OrderedDict
from loguru import logger


@dataclass
class CacheEntry:
    """A single cache entry."""
    key: str
    response: Any
    timestamp: float
    hits: int = 0
    scene_type: str = ""
    health_bucket: str = ""  # low/medium/high
    combat_state: bool = False


class LLMResponseCache:
    """
    Intelligent cache for LLM responses.
    
    Features:
    - TTL-based expiration (default 120 seconds)
    - LRU eviction when max size reached
    - Scene-aware similarity matching
    - Hit rate tracking for optimization
    """
    
    def __init__(
        self,
        max_size: int = 200,
        ttl_seconds: float = 120.0,
        enable_similarity: bool = True
    ):
        """
        Initialize response cache.
        
        Args:
            max_size: Maximum number of entries
            ttl_seconds: Time-to-live for cache entries
            enable_similarity: Enable fuzzy matching for similar contexts
        """
        self.max_size = max_size
        self.ttl = ttl_seconds
        self.enable_similarity = enable_similarity
        
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._hits = 0
        self._misses = 0
        
        logger.info(
            f"LLM Response Cache initialized: max_size={max_size}, "
            f"ttl={ttl_seconds}s, similarity={enable_similarity}"
        )
    
    def _make_key(
        self,
        scene_type: str,
        health: float,
        in_combat: bool,
        available_actions: Tuple[str, ...],
        context_hash: Optional[str] = None
    ) -> str:
        """
        Generate cache key from game state.
        
        Args:
            scene_type: Scene classification
            health: Health percentage (0-100)
            in_combat: Combat state
            available_actions: Tuple of available actions
            context_hash: Optional hash of additional context
            
        Returns:
            Cache key string
        """
        # Bucket health into categories
        if health < 30:
            health_bucket = "low"
        elif health < 70:
            health_bucket = "medium"
        else:
            health_bucket = "high"
        
        # Create key from state components
        actions_str = "|".join(sorted(available_actions))
        
        if context_hash:
            key_parts = [scene_type, health_bucket, str(in_combat), actions_str, context_hash]
        else:
            key_parts = [scene_type, health_bucket, str(in_combat), actions_str]
        
        key = hashlib.md5("|".join(key_parts).encode()).hexdigest()
        return key
    
    def _health_bucket(self, health: float) -> str:
        """Categorize health level."""
        if health < 30:
            return "low"
        elif health < 70:
            return "medium"
        else:
            return "high"
    
    def get(
        self,
        scene_type: str,
        health: float,
        in_combat: bool,
        available_actions: Tuple[str, ...],
        context_hash: Optional[str] = None
    ) -> Optional[Any]:
        """
        Retrieve cached response if available.
        
        Args:
            scene_type: Scene classification
            health: Health percentage
            in_combat: Combat state
            available_actions: Available actions
            context_hash: Optional additional context
            
        Returns:
            Cached response or None
        """
        # Try exact match first
        key = self._make_key(scene_type, health, in_combat, available_actions, context_hash)
        
        if key in self._cache:
            entry = self._cache[key]
            
            # Check TTL
            age = time.time() - entry.timestamp
            if age < self.ttl:
                # Move to end (LRU)
                self._cache.move_to_end(key)
                entry.hits += 1
                self._hits += 1
                
                logger.debug(
                    f"Cache HIT: {scene_type}/{self._health_bucket(health)}/combat={in_combat} "
                    f"(age={age:.1f}s, hits={entry.hits})"
                )
                return entry.response
            else:
                # Expired, remove
                del self._cache[key]
                logger.debug(f"Cache entry expired: age={age:.1f}s > ttl={self.ttl}s")
        
        # Try similarity matching if enabled
        if self.enable_similarity:
            similar = self._find_similar(scene_type, health, in_combat)
            if similar:
                self._hits += 1
                logger.debug(
                    f"Cache SIMILAR HIT: {scene_type}/{self._health_bucket(health)} "
                    f"matched {similar.scene_type}/{similar.health_bucket}"
                )
                return similar.response
        
        self._misses += 1
        logger.debug(f"Cache MISS: {scene_type}/{self._health_bucket(health)}/combat={in_combat}")
        return None
    
    def _find_similar(
        self,
        scene_type: str,
        health: float,
        in_combat: bool
    ) -> Optional[CacheEntry]:
        """
        Find similar cache entry using fuzzy matching.
        
        Args:
            scene_type: Target scene type
            health: Target health
            in_combat: Target combat state
            
        Returns:
            Similar entry or None
        """
        health_bucket = self._health_bucket(health)
        
        # Look for entries with same scene + health bucket + combat state
        for entry in reversed(self._cache.values()):
            age = time.time() - entry.timestamp
            if age >= self.ttl:
                continue
                
            if (entry.scene_type == scene_type and
                entry.health_bucket == health_bucket and
                entry.combat_state == in_combat):
                return entry
        
        return None
    
    def put(
        self,
        scene_type: str,
        health: float,
        in_combat: bool,
        available_actions: Tuple[str, ...],
        response: Any,
        context_hash: Optional[str] = None
    ):
        """
        Store response in cache.
        
        Args:
            scene_type: Scene classification
            health: Health percentage
            in_combat: Combat state
            available_actions: Available actions
            response: Response to cache
            context_hash: Optional additional context
        """
        key = self._make_key(scene_type, health, in_combat, available_actions, context_hash)
        
        # Evict oldest if at capacity
        if len(self._cache) >= self.max_size:
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
            logger.debug(f"Cache evicted oldest entry (LRU)")
        
        # Store entry
        entry = CacheEntry(
            key=key,
            response=response,
            timestamp=time.time(),
            scene_type=scene_type,
            health_bucket=self._health_bucket(health),
            combat_state=in_combat
        )
        
        self._cache[key] = entry
        logger.debug(
            f"Cache PUT: {scene_type}/{entry.health_bucket}/combat={in_combat} "
            f"(size={len(self._cache)}/{self.max_size})"
        )
    
    def clear(self):
        """Clear all cache entries."""
        self._cache.clear()
        logger.info("Cache cleared")
    
    def stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dict with hit rate, size, and other metrics
        """
        total = self._hits + self._misses
        hit_rate = (self._hits / total * 100) if total > 0 else 0.0
        
        return {
            "size": len(self._cache),
            "max_size": self.max_size,
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": hit_rate,
            "ttl_seconds": self.ttl
        }
    
    def prune_expired(self):
        """Remove expired entries."""
        now = time.time()
        expired = [
            key for key, entry in self._cache.items()
            if (now - entry.timestamp) >= self.ttl
        ]
        
        for key in expired:
            del self._cache[key]
        
        if expired:
            logger.debug(f"Pruned {len(expired)} expired cache entries")
