"""
Meta-MoE Router

Routes queries to appropriate expert models on Cygnus (AMD 2x7900XT).
Each expert is a separate 4B parameter model specialized for one domain.

Architecture:
- 10 expert models on Cygnus (ports 1234-1243)
- Router determines which experts to query based on task
- Aggregates responses and synthesizes
"""

from __future__ import annotations

import asyncio
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass
from enum import Enum

from loguru import logger

from .openai_client import OpenAIClient
from .expert_arbiter import ExpertArbiter, ExpertSelectionContext, ExpertDomain as ArbiterExpertDomain


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
class ExpertConfig:
    """Configuration for a single expert."""
    domain: ExpertDomain
    base_url: str           # e.g., "http://192.168.1.50:1234/v1"
    model_name: str         # e.g., "Qwen2-VL-4B"
    specialization: str     # Description of what this expert does


@dataclass
class ExpertResponse:
    """Response from a single expert."""
    domain: ExpertDomain
    content: str
    confidence: float
    execution_time: float


class MetaMoERouter:
    """
    Routes queries to appropriate expert models on Cygnus.
    
    This is NOT a single MoE model - it's a meta-orchestrator
    that routes to 10 separate 4B models, each specialized.
    """
    
    def __init__(
        self,
        cygnus_ip: str = "192.168.1.50",
        macbook_ip: Optional[str] = None,
        enable_macbook_fallback: bool = False
    ):
        """
        Initialize Meta-MoE router.
        
        Args:
            cygnus_ip: IP address of Cygnus (AMD 2x7900XT)
            macbook_ip: Optional IP of MacBook Pro (large MoE model)
            enable_macbook_fallback: Whether to use MacBook as fallback
        """
        self.cygnus_ip = cygnus_ip
        self.macbook_ip = macbook_ip
        self.enable_macbook_fallback = enable_macbook_fallback
        
        # Configure 10 experts on Cygnus
        self.experts: Dict[ExpertDomain, ExpertConfig] = {
            ExpertDomain.VISION: ExpertConfig(
                domain=ExpertDomain.VISION,
                base_url=f"http://{cygnus_ip}:1234/v1",
                model_name="Qwen2-VL-4B",
                specialization="Visual analysis, image understanding, scene description"
            ),
            ExpertDomain.LOGIC: ExpertConfig(
                domain=ExpertDomain.LOGIC,
                base_url=f"http://{cygnus_ip}:1235/v1",
                model_name="DeepSeek-Coder-4B",
                specialization="Symbolic reasoning, formal logic, verification"
            ),
            ExpertDomain.MEMORY: ExpertConfig(
                domain=ExpertDomain.MEMORY,
                base_url=f"http://{cygnus_ip}:1236/v1",
                model_name="Phi-4-mini",
                specialization="Memory retrieval, pattern matching, recall"
            ),
            ExpertDomain.ACTION: ExpertConfig(
                domain=ExpertDomain.ACTION,
                base_url=f"http://{cygnus_ip}:1237/v1",
                model_name="TinyLlama-4B",
                specialization="Action planning, decision making, execution"
            ),
            ExpertDomain.EMOTION: ExpertConfig(
                domain=ExpertDomain.EMOTION,
                base_url=f"http://{cygnus_ip}:1238/v1",
                model_name="EmotiLLM-4B",
                specialization="Emotional intelligence, empathy, sentiment"
            ),
            ExpertDomain.REASONING: ExpertConfig(
                domain=ExpertDomain.REASONING,
                base_url=f"http://{cygnus_ip}:1239/v1",
                model_name="Mistral-4B",
                specialization="Analytical reasoning, inference, deduction"
            ),
            ExpertDomain.PLANNING: ExpertConfig(
                domain=ExpertDomain.PLANNING,
                base_url=f"http://{cygnus_ip}:1240/v1",
                model_name="CodeLlama-4B",
                specialization="Strategic planning, goal decomposition"
            ),
            ExpertDomain.LANGUAGE: ExpertConfig(
                domain=ExpertDomain.LANGUAGE,
                base_url=f"http://{cygnus_ip}:1241/v1",
                model_name="Llama3.2-4B",
                specialization="Natural language, communication, translation"
            ),
            ExpertDomain.ANALYSIS: ExpertConfig(
                domain=ExpertDomain.ANALYSIS,
                base_url=f"http://{cygnus_ip}:1242/v1",
                model_name="Phi-4-data",
                specialization="Data analysis, pattern detection, insights"
            ),
            ExpertDomain.SYNTHESIS: ExpertConfig(
                domain=ExpertDomain.SYNTHESIS,
                base_url=f"http://{cygnus_ip}:1243/v1",
                model_name="Yi-4B",
                specialization="Integration, synthesis, unification"
            ),
        }
        
        # Create OpenAI clients for each expert
        self.expert_clients: Dict[ExpertDomain, OpenAIClient] = {}
        for domain, config in self.experts.items():
            self.expert_clients[domain] = OpenAIClient(
                model=config.model_name,
                base_url=config.base_url,
                timeout=60
            )
        
        # MacBook fallback (large MoE model)
        self.macbook_client: Optional[OpenAIClient] = None
        if macbook_ip and enable_macbook_fallback:
            self.macbook_client = OpenAIClient(
                model="Qwen2.5-14B-MoE",  # Or Mixtral-8x7B
                base_url=f"http://{macbook_ip}:2000/v1",
                timeout=120
            )
        
        # Expert Arbiter for context-aware selection
        self.arbiter: Optional[ExpertArbiter] = None  # Will be set by consciousness layer
        
        # Statistics
        self.stats = {
            'total_queries': 0,
            'expert_calls': {domain: 0 for domain in ExpertDomain},
            'macbook_calls': 0,
            'avg_latency': 0.0,
            'arbiter_selections': 0,
            'fallback_selections': 0,
        }
        
        logger.info(
            f"[META-MoE] Router initialized | "
            f"Cygnus: {cygnus_ip} | "
            f"Experts: {len(self.experts)} | "
            f"MacBook fallback: {enable_macbook_fallback}"
        )
    
    async def _select_experts(
        self,
        query: str,
        subsystem_inputs: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Set[ExpertDomain]:
        """
        Determine which experts should process this query using ExpertArbiter.
        
        Args:
            query: User query
            subsystem_inputs: Subsystem data
            context: Additional context
            
        Returns:
            Set of expert domains to query
        """
        # Use ExpertArbiter if available (context-aware selection with memory)
        if self.arbiter:
            selection_context = ExpertSelectionContext(
                query=query,
                subsystem_inputs=subsystem_inputs,
                user_context=context
            )
            
            selected_arbiter = await self.arbiter.select_experts(selection_context)
            self.stats['arbiter_selections'] += 1
            
            # Convert arbiter domains to router domains (same enum values)
            selected = {
                ExpertDomain(domain.value) for domain in selected_arbiter
            }
            
            logger.info(f"[META-MoE] Arbiter selected {len(selected)} experts")
            return selected
        
        # Fallback: Simple keyword-based selection (if arbiter not available)
        logger.warning("[META-MoE] Arbiter not available, using fallback selection")
        self.stats['fallback_selections'] += 1
        
        selected = set()
        query_lower = query.lower()
        
        # Vision: If images, visual analysis, perception
        if 'image' in query_lower or 'see' in query_lower or 'vision' in subsystem_inputs:
            selected.add(ExpertDomain.VISION)
        
        # Logic: If reasoning, verification, logic needed
        if any(kw in query_lower for kw in ['logic', 'reason', 'verify', 'proof', 'valid']):
            selected.add(ExpertDomain.LOGIC)
        
        # Memory: If recall, history, past events
        if any(kw in query_lower for kw in ['remember', 'recall', 'past', 'history', 'before']):
            selected.add(ExpertDomain.MEMORY)
        
        # Action: If planning actions, decisions
        if any(kw in query_lower for kw in ['should', 'action', 'do', 'decide', 'choose']):
            selected.add(ExpertDomain.ACTION)
        
        # Emotion: If emotions, feelings, empathy
        if any(kw in query_lower for kw in ['feel', 'emotion', 'mood', 'sentiment', 'empathy']):
            selected.add(ExpertDomain.EMOTION)
        
        # Analysis: If data, patterns, insights
        if any(kw in query_lower for kw in ['analyze', 'pattern', 'trend', 'insight', 'data']):
            selected.add(ExpertDomain.ANALYSIS)
        
        # Always include: Reasoning, Language, Synthesis
        selected.add(ExpertDomain.REASONING)  # Core reasoning
        selected.add(ExpertDomain.LANGUAGE)   # Natural language understanding
        selected.add(ExpertDomain.SYNTHESIS)  # Final synthesis
        
        # LifeOps specific: Add planning for life queries
        if context and 'life' in str(context).lower():
            selected.add(ExpertDomain.PLANNING)
        
        return selected
    
    async def route_query(
        self,
        query: str,
        subsystem_inputs: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Route query to appropriate experts and synthesize response.
        
        Args:
            query: User query
            subsystem_inputs: Subsystem data
            context: Additional context
            
        Returns:
            Synthesized response from experts
        """
        import time
        start_time = time.time()
        
        # Select experts
        selected_experts = self._select_experts(query, subsystem_inputs, context)
        
        logger.info(
            f"[META-MoE] Routing query to {len(selected_experts)} experts: "
            f"{[e.value for e in selected_experts]}"
        )
        
        # Query experts in parallel
        tasks = []
        for domain in selected_experts:
            task = self._query_expert(domain, query, subsystem_inputs, context)
            tasks.append((domain, task))
        
        # Execute in parallel
        results = await asyncio.gather(*[task for _, task in tasks], return_exceptions=True)
        
        # Collect responses
        expert_responses: List[ExpertResponse] = []
        for (domain, _), result in zip(tasks, results):
            if isinstance(result, ExpertResponse):
                expert_responses.append(result)
                self.stats['expert_calls'][domain] += 1
            else:
                logger.warning(f"[META-MoE] Expert {domain.value} failed: {result}")
        
        # If no experts succeeded, try MacBook fallback
        if not expert_responses and self.macbook_client:
            logger.warning("[META-MoE] All Cygnus experts failed, falling back to MacBook")
            response = await self._query_macbook(query, subsystem_inputs, context)
            self.stats['macbook_calls'] += 1
            return response
        
        # Synthesize responses (use SYNTHESIS expert's response as base)
        synthesis_response = next(
            (r for r in expert_responses if r.domain == ExpertDomain.SYNTHESIS),
            expert_responses[0] if expert_responses else None
        )
        
        if not synthesis_response:
            return "Error: No expert responses available"
        
        # Update stats
        latency = time.time() - start_time
        self.stats['total_queries'] += 1
        self.stats['avg_latency'] = (
            (self.stats['avg_latency'] * (self.stats['total_queries'] - 1) + latency) /
            self.stats['total_queries']
        )
        
        logger.info(
            f"[META-MoE] Query complete | "
            f"Experts: {len(expert_responses)} | "
            f"Latency: {latency:.2f}s"
        )
        
        return synthesis_response.content
    
    async def _query_expert(
        self,
        domain: ExpertDomain,
        query: str,
        subsystem_inputs: Dict[str, Any],
        context: Optional[Dict[str, Any]]
    ) -> ExpertResponse:
        """Query a single expert."""
        import time
        start_time = time.time()
        
        config = self.experts[domain]
        client = self.expert_clients[domain]
        
        # Build expert-specific prompt
        system_prompt = (
            f"You are the {domain.value.upper()} Expert in a Meta-MoE system.\n"
            f"Your specialization: {config.specialization}\n"
            f"Provide focused analysis from your domain perspective."
        )
        
        try:
            result = await client.generate_text(
                prompt=query,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=512  # Small experts, focused responses
            )
            
            execution_time = time.time() - start_time
            
            # Estimate confidence from response length and quality
            confidence = min(0.9, 0.5 + len(result) / 1000)
            
            response = ExpertResponse(
                domain=domain,
                content=result,
                confidence=confidence,
                execution_time=execution_time
            )
            
            # Record result in arbiter for continuous learning
            if self.arbiter:
                query_type = context.get('query_type', 'general') if context else 'general'
                self.arbiter.record_expert_result(
                    domain=ArbiterExpertDomain(domain.value),  # Convert to arbiter enum
                    query_type=query_type,
                    success=True,
                    confidence=confidence,
                    latency=execution_time
                )
            
            return response
            
        except Exception as e:
            logger.error(f"[META-MoE] Expert {domain.value} failed: {e}")
            
            # Record failure in arbiter
            if self.arbiter:
                query_type = context.get('query_type', 'general') if context else 'general'
                self.arbiter.record_expert_result(
                    domain=ArbiterExpertDomain(domain.value),
                    query_type=query_type,
                    success=False
                )
            
            raise
    
    async def _query_macbook(
        self,
        query: str,
        subsystem_inputs: Dict[str, Any],
        context: Optional[Dict[str, Any]]
    ) -> str:
        """Query MacBook large MoE model as fallback."""
        if not self.macbook_client:
            return "Error: MacBook fallback not configured"
        
        try:
            return await self.macbook_client.generate_text(
                prompt=query,
                system_prompt="You are a large MoE model providing comprehensive analysis.",
                temperature=0.8,
                max_tokens=2048
            )
        except Exception as e:
            logger.error(f"[META-MoE] MacBook fallback failed: {e}")
            return f"Error: All inference backends failed"
    
    def get_stats(self) -> Dict[str, Any]:
        """Get routing statistics."""
        return {
            **self.stats,
            'expert_health': {
                domain.value: self.expert_clients[domain].is_available()
                for domain in ExpertDomain
            },
            'macbook_available': self.macbook_client.is_available() if self.macbook_client else False
        }
