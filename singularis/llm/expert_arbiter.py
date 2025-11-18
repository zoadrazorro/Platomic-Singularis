"""
Expert Arbiter - Context-aware expert selection for Meta-MoE

Intelligently routes queries to appropriate expert models on Cygnus using:
1. Query context analysis (not keyword matching)
2. Historical performance tracking
3. Subsystem consensus evaluation
4. Dynamic expert selection based on success patterns

Based on ActionArbiter pattern from Skyrim AGI.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Any
from enum import Enum

from loguru import logger

try:
    from ..core.runtime_flags import LOCAL_ONLY_LLM
except ImportError:
    LOCAL_ONLY_LLM = False


class ExpertDomain(Enum):
    """Expert domains in Meta-MoE."""
    VISION = "vision"                # Visual analysis, image understanding
    LOGIC = "logic"                  # Symbolic reasoning, formal logic
    MEMORY = "memory"                # Memory retrieval, pattern matching
    ACTION = "action"                # Action planning, decision making
    EMOTION = "emotion"              # Emotional intelligence, empathy
    REASONING = "reasoning"          # Analytical reasoning
    PLANNING = "planning"            # Strategic planning
    LANGUAGE = "language"            # Natural language, communication
    ANALYSIS = "analysis"            # Data analysis, insights
    SYNTHESIS = "synthesis"          # Integration, synthesis


@dataclass
class ExpertSelectionContext:
    """Context for expert selection decision."""
    query: str
    subsystem_inputs: Dict[str, Any]
    user_context: Optional[Dict[str, Any]] = None
    query_type: Optional[str] = None  # 'life_query', 'pattern', 'intervention', etc.
    timestamp: float = field(default_factory=time.time)


@dataclass
class ExpertPerformance:
    """Tracks performance of an expert for a query type."""
    domain: ExpertDomain
    query_type: str
    success_count: int = 0
    failure_count: int = 0
    avg_confidence: float = 0.0
    avg_latency: float = 0.0
    last_used: float = 0.0
    
    def success_rate(self) -> float:
        """Calculate success rate."""
        total = self.success_count + self.failure_count
        return self.success_count / total if total > 0 else 0.5
    
    def update_success(self, confidence: float, latency: float):
        """Record successful query."""
        self.success_count += 1
        total = self.success_count + self.failure_count
        # Running average
        self.avg_confidence = (self.avg_confidence * (total - 1) + confidence) / total
        self.avg_latency = (self.avg_latency * (total - 1) + latency) / total
        self.last_used = time.time()
    
    def update_failure(self):
        """Record failed query."""
        self.failure_count += 1
        self.last_used = time.time()


class ExpertArbiter:
    """
    Context-aware expert selection arbiter.
    
    Uses reasoning and historical performance to decide which experts
    should handle each query, rather than simple keyword matching.
    """
    
    def __init__(
        self,
        consciousness_layer: Optional[Any] = None,
        enable_learning: bool = True
    ):
        """
        Initialize expert arbiter.
        
        Args:
            consciousness_layer: Optional UnifiedConsciousnessLayer for meta-reasoning
            enable_learning: Whether to learn from expert performance
        """
        self.consciousness = consciousness_layer
        self.enable_learning = enable_learning
        
        # Performance tracking per (expert, query_type)
        self.performance: Dict[tuple[ExpertDomain, str], ExpertPerformance] = {}
        
        # Expert availability
        self.expert_health: Dict[ExpertDomain, bool] = {
            domain: True for domain in ExpertDomain
        }
        
        # Statistics
        self.stats = {
            'total_selections': 0,
            'by_domain': {domain: 0 for domain in ExpertDomain},
            'by_query_type': {},
            'consciousness_consultations': 0,
            'local_selections': 0,
            'selection_time_total': 0.0,
        }
        
        logger.info("[EXPERT-ARBITER] Initialized with context-aware selection")
    
    async def select_experts(
        self,
        context: ExpertSelectionContext
    ) -> Set[ExpertDomain]:
        """
        Select appropriate experts for a query using context-aware reasoning.
        
        Args:
            context: Query context including subsystems, user context, etc.
            
        Returns:
            Set of expert domains to query
        """
        start_time = time.time()
        
        # Categorize query type
        query_type = self._categorize_query(context)
        context.query_type = query_type
        
        logger.info(f"[EXPERT-ARBITER] Selecting experts for query type: {query_type}")
        
        # Strategy 1: Use consciousness layer for complex selection (if available)
        if self.consciousness and self._should_use_consciousness(context):
            selected = await self._select_via_consciousness(context)
            self.stats['consciousness_consultations'] += 1
        else:
            # Strategy 2: Use fast local selection based on context + performance
            selected = self._select_via_local_reasoning(context)
            self.stats['local_selections'] += 1
        
        # Always include synthesis expert
        selected.add(ExpertDomain.SYNTHESIS)
        
        # Update stats
        self.stats['total_selections'] += 1
        self.stats['by_query_type'][query_type] = self.stats['by_query_type'].get(query_type, 0) + 1
        for domain in selected:
            self.stats['by_domain'][domain] += 1
        
        elapsed = time.time() - start_time
        self.stats['selection_time_total'] += elapsed
        
        logger.info(
            f"[EXPERT-ARBITER] Selected {len(selected)} experts: "
            f"{[e.value for e in selected]} ({elapsed:.3f}s)"
        )
        
        return selected
    
    def _categorize_query(self, context: ExpertSelectionContext) -> str:
        """
        Categorize query type based on context.
        
        Returns:
            Query type string (e.g., 'life_query', 'pattern_interpretation', etc.)
        """
        query_lower = context.query.lower()
        subsystems = context.subsystem_inputs
        user_ctx = context.user_context or {}
        
        # Check for explicit type
        if 'query_type' in user_ctx:
            return user_ctx['query_type']
        
        # Detect from subsystem inputs
        if 'pattern_data' in subsystems:
            return 'pattern_interpretation'
        
        if 'decision_type' in subsystems:
            if subsystems['decision_type'] == 'intervention':
                return 'intervention_decision'
        
        # Detect from query content
        if any(kw in query_lower for kw in ['sleep', 'exercise', 'health', 'heart rate']):
            return 'life_query_health'
        
        if any(kw in query_lower for kw in ['pattern', 'routine', 'habit', 'trend']):
            return 'life_query_pattern'
        
        if any(kw in query_lower for kw in ['feel', 'mood', 'emotion', 'stressed']):
            return 'life_query_emotion'
        
        if any(kw in query_lower for kw in ['should', 'recommend', 'suggest', 'what to do']):
            return 'action_recommendation'
        
        if any(kw in query_lower for kw in ['why', 'explain', 'reason', 'cause']):
            return 'causal_analysis'
        
        # Default
        return 'general_query'
    
    def _should_use_consciousness(self, context: ExpertSelectionContext) -> bool:
        """
        Determine if we should use consciousness layer for selection.
        
        Use consciousness for:
        - Complex multi-domain queries
        - New/rare query types
        - Conflicting subsystem inputs
        
        Use local reasoning for:
        - Simple, common query types
        - Clear domain match
        - Good historical performance
        """
        query_type = context.query_type
        
        # Use local for common query types with good performance
        common_types = ['life_query_health', 'life_query_pattern', 'general_query']
        if query_type in common_types:
            # Check if we have good historical performance
            relevant_perf = [
                perf for (domain, qtype), perf in self.performance.items()
                if qtype == query_type and perf.success_rate() > 0.7
            ]
            if len(relevant_perf) >= 3:
                # We have proven experts for this query type
                return False
        
        # Use consciousness for rare/new query types
        query_count = self.stats['by_query_type'].get(query_type, 0)
        if query_count < 5:
            # Query type is rare, use consciousness
            return True
        
        # Use consciousness if subsystems disagree
        if len(context.subsystem_inputs) > 3:
            # Multiple subsystems involved - may need coordination
            return True
        
        # Default: use local reasoning
        return False
    
    async def _select_via_consciousness(
        self,
        context: ExpertSelectionContext
    ) -> Set[ExpertDomain]:
        """
        Use consciousness layer to select experts via meta-reasoning.
        
        This queries the consciousness layer to decide which experts
        are most appropriate for the given context.
        """
        if not self.consciousness:
            logger.warning("[EXPERT-ARBITER] Consciousness not available, falling back to local")
            return self._select_via_local_reasoning(context)
        
        # Build prompt for consciousness
        prompt = self._build_selection_prompt(context)
        
        try:
            # Query consciousness (lightweight - just for selection)
            response = await self.consciousness.process(
                query=prompt,
                subsystem_inputs={
                    'expert_selection': {
                        'available_experts': [e.value for e in ExpertDomain],
                        'query_type': context.query_type,
                        'subsystems': list(context.subsystem_inputs.keys())
                    }
                },
                context=context.user_context or {}
            )
            
            # Parse expert selection from response
            selected = self._parse_expert_selection(response.response)
            
            logger.info(f"[EXPERT-ARBITER] Consciousness selected: {[e.value for e in selected]}")
            
            return selected
            
        except Exception as e:
            logger.error(f"[EXPERT-ARBITER] Consciousness selection failed: {e}, falling back")
            return self._select_via_local_reasoning(context)
    
    def _select_via_local_reasoning(
        self,
        context: ExpertSelectionContext
    ) -> Set[ExpertDomain]:
        """
        Fast local expert selection based on query type and performance history.
        
        This uses learned patterns and heuristics without calling LLMs.
        """
        query_type = context.query_type
        selected = set()
        
        # Core experts based on query type
        type_to_experts = {
            'life_query_health': {
                ExpertDomain.ANALYSIS,    # Analyze health data
                ExpertDomain.MEMORY,      # Recall past patterns
                ExpertDomain.REASONING,   # Reason about health
                ExpertDomain.LANGUAGE,    # Communicate clearly
            },
            'life_query_pattern': {
                ExpertDomain.ANALYSIS,    # Pattern detection
                ExpertDomain.MEMORY,      # Historical context
                ExpertDomain.REASONING,   # Pattern reasoning
                ExpertDomain.LANGUAGE,    # Explain patterns
            },
            'life_query_emotion': {
                ExpertDomain.EMOTION,     # Emotional analysis
                ExpertDomain.MEMORY,      # Emotional history
                ExpertDomain.REASONING,   # Emotional reasoning
                ExpertDomain.LANGUAGE,    # Empathetic communication
            },
            'pattern_interpretation': {
                ExpertDomain.ANALYSIS,    # Pattern analysis
                ExpertDomain.LOGIC,       # Logical validation
                ExpertDomain.MEMORY,      # Context from memory
                ExpertDomain.REASONING,   # Deep reasoning
            },
            'intervention_decision': {
                ExpertDomain.EMOTION,     # Emotional consideration
                ExpertDomain.REASONING,   # Logical evaluation
                ExpertDomain.ACTION,      # Action planning
                ExpertDomain.PLANNING,    # Strategic timing
            },
            'action_recommendation': {
                ExpertDomain.ACTION,      # Action planning
                ExpertDomain.PLANNING,    # Strategic planning
                ExpertDomain.REASONING,   # Reason about actions
                ExpertDomain.MEMORY,      # Learn from past
            },
            'causal_analysis': {
                ExpertDomain.LOGIC,       # Causal logic
                ExpertDomain.REASONING,   # Deep reasoning
                ExpertDomain.MEMORY,      # Historical patterns
                ExpertDomain.ANALYSIS,    # Data analysis
            },
            'general_query': {
                ExpertDomain.LANGUAGE,    # Language understanding
                ExpertDomain.REASONING,   # General reasoning
                ExpertDomain.MEMORY,      # Context
            },
        }
        
        # Get base experts for query type
        base_experts = type_to_experts.get(query_type, set())
        selected.update(base_experts)
        
        # Add context-specific experts
        subsystems = context.subsystem_inputs
        
        # If vision data present, add vision expert
        if any(k in subsystems for k in ['vision', 'image', 'visual', 'perception']):
            selected.add(ExpertDomain.VISION)
        
        # If emotional data present, add emotion expert
        if any(k in subsystems for k in ['emotion', 'mood', 'sentiment']):
            selected.add(ExpertDomain.EMOTION)
        
        # If memory/history needed
        if any(k in subsystems for k in ['memory', 'history', 'past']):
            selected.add(ExpertDomain.MEMORY)
        
        # Use performance history to refine selection
        if self.enable_learning:
            selected = self._refine_with_performance(selected, query_type)
        
        # Filter out unhealthy experts
        selected = {e for e in selected if self.expert_health.get(e, True)}
        
        # Ensure minimum 3 experts
        if len(selected) < 3:
            # Add high-performing general experts
            general_experts = [ExpertDomain.REASONING, ExpertDomain.LANGUAGE, ExpertDomain.ANALYSIS]
            for expert in general_experts:
                if len(selected) >= 3:
                    break
                if expert not in selected and self.expert_health.get(expert, True):
                    selected.add(expert)
        
        return selected
    
    def _refine_with_performance(
        self,
        selected: Set[ExpertDomain],
        query_type: str
    ) -> Set[ExpertDomain]:
        """
        Refine expert selection based on historical performance.
        
        - Keep high-performing experts
        - Remove low-performing experts
        - Add alternative experts if performance is poor
        """
        refined = set()
        
        for expert in selected:
            perf_key = (expert, query_type)
            
            if perf_key in self.performance:
                perf = self.performance[perf_key]
                
                # Keep if success rate > 60%
                if perf.success_rate() >= 0.6:
                    refined.add(expert)
                elif perf.success_count + perf.failure_count < 3:
                    # Not enough data, keep
                    refined.add(expert)
                else:
                    # Poor performance, skip
                    logger.info(
                        f"[EXPERT-ARBITER] Skipping {expert.value} for {query_type} "
                        f"(success rate: {perf.success_rate():.1%})"
                    )
            else:
                # No history, include
                refined.add(expert)
        
        # If we filtered out too many, add some back
        if len(refined) < len(selected) * 0.6:
            refined = selected  # Restore original selection
        
        return refined
    
    def _build_selection_prompt(self, context: ExpertSelectionContext) -> str:
        """Build prompt for consciousness-based expert selection."""
        available = [e.value for e in ExpertDomain]
        
        prompt = f"""Expert Selection Task:

Query: "{context.query}"
Query Type: {context.query_type}

Available Experts:
{', '.join(available)}

Subsystem Inputs: {list(context.subsystem_inputs.keys())}

Select 3-5 experts that are most appropriate for this query.
Consider:
1. Query type and domain requirements
2. Subsystem data available
3. Need for specialized vs general reasoning

Return selected experts as comma-separated list."""
        
        return prompt
    
    def _parse_expert_selection(self, response: str) -> Set[ExpertDomain]:
        """Parse expert selection from consciousness response."""
        selected = set()
        response_lower = response.lower()
        
        for domain in ExpertDomain:
            if domain.value in response_lower:
                selected.add(domain)
        
        # Fallback if no experts found
        if not selected:
            logger.warning("[EXPERT-ARBITER] No experts parsed, using defaults")
            selected = {ExpertDomain.REASONING, ExpertDomain.LANGUAGE, ExpertDomain.ANALYSIS}
        
        return selected
    
    def record_expert_result(
        self,
        domain: ExpertDomain,
        query_type: str,
        success: bool,
        confidence: float = 0.0,
        latency: float = 0.0
    ):
        """
        Record result of expert query for learning.
        
        Args:
            domain: Expert domain
            query_type: Type of query
            success: Whether expert query succeeded
            confidence: Confidence of result
            latency: Query latency
        """
        if not self.enable_learning:
            return
        
        perf_key = (domain, query_type)
        
        if perf_key not in self.performance:
            self.performance[perf_key] = ExpertPerformance(
                domain=domain,
                query_type=query_type
            )
        
        perf = self.performance[perf_key]
        
        if success:
            perf.update_success(confidence, latency)
        else:
            perf.update_failure()
        
        logger.debug(
            f"[EXPERT-ARBITER] Recorded {domain.value} for {query_type}: "
            f"success={success}, success_rate={perf.success_rate():.1%}"
        )
    
    def update_expert_health(self, domain: ExpertDomain, is_healthy: bool):
        """
        Update health status of an expert.
        
        Args:
            domain: Expert domain
            is_healthy: Whether expert is healthy/available
        """
        self.expert_health[domain] = is_healthy
        
        if not is_healthy:
            logger.warning(f"[EXPERT-ARBITER] Expert {domain.value} marked unhealthy")
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get performance report for all experts."""
        report = {
            'by_expert': {},
            'by_query_type': {},
            'top_performers': [],
            'poor_performers': []
        }
        
        # Aggregate by expert
        for (domain, query_type), perf in self.performance.items():
            if domain.value not in report['by_expert']:
                report['by_expert'][domain.value] = {
                    'total_queries': 0,
                    'success_rate': 0.0,
                    'query_types': []
                }
            
            report['by_expert'][domain.value]['total_queries'] += perf.success_count + perf.failure_count
            report['by_expert'][domain.value]['query_types'].append(query_type)
        
        # Calculate success rates
        for domain_name in report['by_expert']:
            domain_enum = next(e for e in ExpertDomain if e.value == domain_name)
            relevant_perfs = [
                p for (d, _), p in self.performance.items() if d == domain_enum
            ]
            if relevant_perfs:
                avg_success = sum(p.success_rate() for p in relevant_perfs) / len(relevant_perfs)
                report['by_expert'][domain_name]['success_rate'] = avg_success
        
        # Find top and poor performers
        expert_scores = [
            (domain, data['success_rate'])
            for domain, data in report['by_expert'].items()
        ]
        expert_scores.sort(key=lambda x: x[1], reverse=True)
        
        report['top_performers'] = expert_scores[:3]
        report['poor_performers'] = [x for x in expert_scores if x[1] < 0.5]
        
        return report
    
    def get_stats(self) -> Dict[str, Any]:
        """Get arbiter statistics."""
        avg_selection_time = (
            self.stats['selection_time_total'] / self.stats['total_selections']
            if self.stats['total_selections'] > 0 else 0.0
        )
        
        return {
            **self.stats,
            'avg_selection_time': avg_selection_time,
            'performance_entries': len(self.performance),
            'consciousness_ratio': (
                self.stats['consciousness_consultations'] / self.stats['total_selections']
                if self.stats['total_selections'] > 0 else 0.0
            )
        }
