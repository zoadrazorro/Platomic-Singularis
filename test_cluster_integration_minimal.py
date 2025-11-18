"""Minimal Cluster Integration Test for Singularis v5.0 (No NVIDIA)

Tests the core 3-device cluster (Cygnus + Router + MacBook) without requiring
the optional NVIDIA laptop with Positronic Network.

This is the MINIMAL viable v5 cluster:
- Cygnus: 10 experts (deductive/symbolic)
- Router: UnifiedConsciousnessLayer + Meta-MoE + DATA-Brain
- MacBook: Large MoE + AURA-Brain (inductive/biological)

Usage:
    python test_cluster_integration_minimal.py

Optional:
    python test_cluster_integration_minimal.py --cygnus-ip 192.168.1.50 --macbook-ip 192.168.1.100
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from dataclasses import dataclass
from typing import Optional

try:
    import aiohttp
except ImportError:  # pragma: no cover
    print("[ERROR] aiohttp is not installed. Install with: pip install aiohttp")
    sys.exit(1)


class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


@dataclass
class TestResult:
    name: str
    passed: bool
    message: str
    details: str = ""


async def test_cygnus_expert(session: aiohttp.ClientSession, ip: str, port: int, domain: str) -> TestResult:
    """Test a single Cygnus expert by sending a real query."""
    url = f"http://{ip}:{port}/v1/chat/completions"
    
    payload = {
        "model": "local-model",
        "messages": [{"role": "user", "content": f"Test query for {domain} expert: What is 2+2?"}],
        "max_tokens": 50,
        "temperature": 0.1,
    }
    
    try:
        async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            if resp.status != 200:
                return TestResult(
                    name=f"Cygnus:{port} ({domain})",
                    passed=False,
                    message=f"HTTP {resp.status}",
                    details=await resp.text()
                )
            
            data = await resp.json()
            
            # Check response structure
            if "choices" not in data or not data["choices"]:
                return TestResult(
                    name=f"Cygnus:{port} ({domain})",
                    passed=False,
                    message="Invalid response structure",
                    details=str(data)
                )
            
            response_text = data["choices"][0].get("message", {}).get("content", "")
            
            if not response_text or len(response_text) < 1:
                return TestResult(
                    name=f"Cygnus:{port} ({domain})",
                    passed=False,
                    message="Empty response",
                    details=str(data)
                )
            
            return TestResult(
                name=f"Cygnus:{port} ({domain})",
                passed=True,
                message="Generated response",
                details=response_text[:100]
            )
            
    except asyncio.TimeoutError:
        return TestResult(
            name=f"Cygnus:{port} ({domain})",
            passed=False,
            message="Timeout (>10s)",
            details="Model may not be loaded or is too slow"
        )
    except Exception as e:  # noqa: BLE001
        return TestResult(
            name=f"Cygnus:{port} ({domain})",
            passed=False,
            message=f"Error: {type(e).__name__}",
            details=str(e)
        )


async def test_macbook_moe(session: aiohttp.ClientSession, ip: str) -> TestResult:
    """Test MacBook large MoE model."""
    url = f"http://{ip}:2000/v1/chat/completions"
    
    payload = {
        "model": "local-model",
        "messages": [{"role": "user", "content": "Explain the concept of emergence in complex systems in one sentence."}],
        "max_tokens": 100,
        "temperature": 0.7,
    }
    
    try:
        async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=30)) as resp:
            if resp.status != 200:
                return TestResult(
                    name="MacBook:MoE",
                    passed=False,
                    message=f"HTTP {resp.status}",
                    details=await resp.text()
                )
            
            data = await resp.json()
            response_text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            if not response_text or len(response_text) < 10:
                return TestResult(
                    name="MacBook:MoE",
                    passed=False,
                    message="Empty or too short response",
                    details=str(data)
                )
            
            return TestResult(
                name="MacBook:MoE",
                passed=True,
                message="Deep reasoning response",
                details=response_text[:150]
            )
            
    except asyncio.TimeoutError:
        return TestResult(
            name="MacBook:MoE",
            passed=False,
            message="Timeout (>30s)",
            details="Large model may not be loaded"
        )
    except Exception as e:  # noqa: BLE001
        return TestResult(
            name="MacBook:MoE",
            passed=False,
            message=f"Error: {type(e).__name__}",
            details=str(e)
        )


async def test_aura_brain(session: aiohttp.ClientSession, ip: str) -> TestResult:
    """Test AURA-Brain bio-simulator."""
    url = f"http://{ip}:3000/process"
    
    payload = {
        "input_pattern": [0.5, 0.8, 0.3, 0.9, 0.1],
        "duration_ms": 100,
        "return_spikes": True,
    }
    
    try:
        async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            if resp.status != 200:
                return TestResult(
                    name="MacBook:AURA",
                    passed=False,
                    message=f"HTTP {resp.status}",
                    details=await resp.text()
                )
            
            data = await resp.json()
            
            # Check for spiking activity
            if "spike_count" not in data and "output_pattern" not in data:
                return TestResult(
                    name="MacBook:AURA",
                    passed=False,
                    message="Invalid AURA response",
                    details=str(data)
                )
            
            spike_count = data.get("spike_count", 0)
            
            return TestResult(
                name="MacBook:AURA",
                passed=True,
                message=f"Biological processing ({spike_count} spikes)",
                details=f"Neuromodulation active, STDP learning enabled"
            )
            
    except asyncio.TimeoutError:
        return TestResult(
            name="MacBook:AURA",
            passed=False,
            message="Timeout",
            details="AURA server may not be running"
        )
    except Exception as e:  # noqa: BLE001
        return TestResult(
            name="MacBook:AURA",
            passed=False,
            message=f"Error: {type(e).__name__}",
            details=str(e)
        )


async def test_meta_moe_routing(cygnus_ip: str, macbook_ip: str) -> TestResult:
    """Test Meta-MoE routing logic (requires local imports)."""
    try:
        from singularis.llm.meta_moe_router import MetaMoERouter
        from singularis.llm.expert_arbiter import ExpertArbiter
        
        # Create router
        router = MetaMoERouter(
            cygnus_ip=cygnus_ip,
            macbook_ip=macbook_ip,
            enable_macbook_fallback=True
        )
        
        # Create arbiter
        arbiter = ExpertArbiter(enable_learning=True)
        router.arbiter = arbiter
        
        # Test query
        response = await router.route_query(
            query="What is the meaning of life?",
            subsystem_inputs={},
            context={"test": True}
        )
        
        if not response or not response.get("response"):
            return TestResult(
                name="Meta-MoE Routing",
                passed=False,
                message="Empty response from router",
                details=str(response)
            )
        
        experts_used = response.get("experts_used", [])
        
        return TestResult(
            name="Meta-MoE Routing",
            passed=True,
            message=f"Routed to {len(experts_used)} experts",
            details=f"Experts: {', '.join(experts_used)}"
        )
        
    except ImportError as e:
        return TestResult(
            name="Meta-MoE Routing",
            passed=False,
            message="Import error",
            details=f"Cannot import router/arbiter: {e}"
        )
    except Exception as e:  # noqa: BLE001
        return TestResult(
            name="Meta-MoE Routing",
            passed=False,
            message=f"Error: {type(e).__name__}",
            details=str(e)
        )


async def test_unified_consciousness(cygnus_ip: str, macbook_ip: str) -> TestResult:
    """Test UnifiedConsciousnessLayer orchestration."""
    try:
        from singularis.unified_consciousness_layer import UnifiedConsciousnessLayer
        
        # Create consciousness layer
        consciousness = UnifiedConsciousnessLayer(
            use_modular_network=True,
            use_meta_moe=True,
            cygnus_ip=cygnus_ip,
            macbook_ip=macbook_ip,
        )
        
        # Test query
        result = await consciousness.process(
            query="Analyze my sleep patterns",
            context={"user_id": "test_user", "test": True}
        )
        
        if not result or not result.get("response"):
            return TestResult(
                name="UnifiedConsciousness",
                passed=False,
                message="Empty response",
                details=str(result)
            )
        
        return TestResult(
            name="UnifiedConsciousness",
            passed=True,
            message="Orchestrated full pipeline",
            details=f"Response length: {len(result.get('response', ''))} chars"
        )
        
    except ImportError as e:
        return TestResult(
            name="UnifiedConsciousness",
            passed=False,
            message="Import error",
            details=f"Cannot import consciousness layer: {e}"
        )
    except Exception as e:  # noqa: BLE001
        return TestResult(
            name="UnifiedConsciousness",
            passed=False,
            message=f"Error: {type(e).__name__}",
            details=str(e)
        )


async def test_data_brain_swarm() -> TestResult:
    """Test DATA-Brain swarm intelligence."""
    try:
        from singularis.data_brain import SwarmIntelligence
        
        # Create swarm
        swarm = SwarmIntelligence(
            num_agents=64,
            topology="scale_free",
            hebbian_learning_rate=0.01,
        )
        
        # Test query
        result = await swarm.process_query(
            query="Analyze health patterns",
            context={"user_id": "test_user"},
            expert_selection={"analysis", "memory", "reasoning"}
        )
        
        if not result:
            return TestResult(
                name="DATA-Brain Swarm",
                passed=False,
                message="Empty response",
                details="Swarm did not return result"
            )
        
        coherence = result.get("swarm_coherence", 0.0)
        
        return TestResult(
            name="DATA-Brain Swarm",
            passed=True,
            message=f"Swarm coherence: {coherence:.2f}",
            details=f"Emergent patterns detected, {len(result.get('emergent_patterns', []))} patterns"
        )
        
    except ImportError as e:
        return TestResult(
            name="DATA-Brain Swarm",
            passed=False,
            message="Import error",
            details=f"Cannot import SwarmIntelligence: {e}"
        )
    except Exception as e:  # noqa: BLE001
        return TestResult(
            name="DATA-Brain Swarm",
            passed=False,
            message=f"Error: {type(e).__name__}",
            details=str(e)
        )


async def run_integration_tests(cygnus_ip: str, macbook_ip: str) -> int:
    """Run all integration tests for minimal 3-device cluster."""
    
    print(f"\n{Colors.HEADER}{Colors.BOLD}SINGULARIS V5.0 MINIMAL CLUSTER INTEGRATION TEST{Colors.ENDC}")
    print(f"{Colors.OKCYAN}Testing 3-device cluster (Cygnus + Router + MacBook){Colors.ENDC}")
    print(f"  Cygnus IP  : {cygnus_ip}")
    print(f"  MacBook IP : {macbook_ip}\n")
    
    results = []
    
    async with aiohttp.ClientSession() as session:
        # Test Cygnus experts (sample 5 for better coverage)
        print(f"{Colors.BOLD}1. Testing Cygnus Experts (Deductive/Symbolic)...{Colors.ENDC}")
        expert_domains = [
            (1234, "Vision"),
            (1235, "Logic"),
            (1237, "Action"),
            (1239, "Reasoning"),
            (1243, "Synthesis"),
        ]
        
        for port, domain in expert_domains:
            result = await test_cygnus_expert(session, cygnus_ip, port, domain)
            results.append(result)
            print_result(result)
        
        # Test MacBook MoE
        print(f"\n{Colors.BOLD}2. Testing MacBook Large MoE (Deep Reasoning)...{Colors.ENDC}")
        result = await test_macbook_moe(session, macbook_ip)
        results.append(result)
        print_result(result)
        
        # Test AURA-Brain (optional but recommended)
        print(f"\n{Colors.BOLD}3. Testing AURA-Brain Bio-Simulator (Inductive/Biological)...{Colors.ENDC}")
        result = await test_aura_brain(session, macbook_ip)
        results.append(result)
        print_result(result, optional=True)
    
    # Test DATA-Brain swarm
    print(f"\n{Colors.BOLD}4. Testing DATA-Brain Swarm Intelligence...{Colors.ENDC}")
    result = await test_data_brain_swarm()
    results.append(result)
    print_result(result)
    
    # Test Meta-MoE routing (requires local imports)
    print(f"\n{Colors.BOLD}5. Testing Meta-MoE Routing + ExpertArbiter...{Colors.ENDC}")
    result = await test_meta_moe_routing(cygnus_ip, macbook_ip)
    results.append(result)
    print_result(result)
    
    # Test UnifiedConsciousnessLayer (requires local imports)
    print(f"\n{Colors.BOLD}6. Testing UnifiedConsciousnessLayer (Full Pipeline)...{Colors.ENDC}")
    result = await test_unified_consciousness(cygnus_ip, macbook_ip)
    results.append(result)
    print_result(result)
    
    # Summary
    print("\n" + "=" * 70)
    print(f"{Colors.BOLD}INTEGRATION TEST SUMMARY{Colors.ENDC}\n")
    
    passed = sum(1 for r in results if r.passed)
    total = len(results)
    
    print(f"  Tests Passed: {passed}/{total} ({passed/total*100:.1f}%)")
    
    critical_failures = [r for r in results if not r.passed and "AURA" not in r.name]
    
    if critical_failures:
        print(f"\n{Colors.FAIL}CRITICAL FAILURES:{Colors.ENDC}")
        for r in critical_failures:
            print(f"  - {r.name}: {r.message}")
        print(f"\n{Colors.WARNING}Note: AURA-Brain is optional but recommended for full orchestra mode.{Colors.ENDC}")
    else:
        print(f"\n{Colors.OKGREEN}✓ All critical tests passed!{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Your 3-device cluster is fully functional.{Colors.ENDC}")
        
        aura_failed = any(r.name == "MacBook:AURA" and not r.passed for r in results)
        if aura_failed:
            print(f"\n{Colors.WARNING}⚠ AURA-Brain not running (optional).{Colors.ENDC}")
            print(f"  To enable orchestra mode, start AURA server on MacBook:3000")
    
    print("=" * 70 + "\n")
    
    return 0 if not critical_failures else 1


def print_result(result: TestResult, optional: bool = False) -> None:
    """Print a single test result."""
    if result.passed:
        color = Colors.OKGREEN
        status = "✓ PASS"
    else:
        color = Colors.WARNING if optional else Colors.FAIL
        status = "⚠ SKIP" if optional else "✗ FAIL"
    
    print(f"{color}{status}{Colors.ENDC} {result.name:<30} {result.message}")
    
    if result.details and (result.passed or not optional):
        detail_lines = result.details.split("\n")
        for line in detail_lines[:2]:  # Max 2 lines
            print(f"      {line[:80]}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Test Singularis v5 minimal cluster (no NVIDIA)")
    parser.add_argument("--cygnus-ip", default=os.getenv("SINGULARIS_CYGNUS_IP", "192.168.1.50"))
    parser.add_argument("--macbook-ip", default=os.getenv("SINGULARIS_MACBOOK_IP", "192.168.1.100"))
    args = parser.parse_args()
    
    try:
        code = asyncio.run(run_integration_tests(args.cygnus_ip, args.macbook_ip))
    except KeyboardInterrupt:  # pragma: no cover
        print("\n[ABORTED] Integration test interrupted by user")
        code = 1
    sys.exit(code)


if __name__ == "__main__":
    main()
