#!/usr/bin/env python3
"""
Singularis Beta v2.4 - Cloud Runtime with HaackLang + SCCE

This is the complete unified AGI system with:
- BeingState: ONE unified state vector
- CoherenceEngine: ONE optimization function
- C_global: ONE target all subsystems optimize
- HaackLang: Polyrhythmic cognitive execution
- SCCE: Temporal cognitive dynamics
- Cloud-only: No local LLMs (Gemini + Claude + GPT)

Philosophy → Mathematics → Cognition → Code → Execution

Run with:
    python run_beta_v2.4_cloud.py --duration 3600 --profile balanced

Author: Singularis Team
Version: 2.4.0-beta
Date: 2025-11-14
"""

import asyncio
import argparse
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Optional

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()


def print_banner():
    """Print the Singularis banner."""
    banner = """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   ███████╗██╗███╗   ██╗ ██████╗ ██╗   ██╗██╗      █████╗ ██████╗ ██╗███████╗   ║
║   ██╔════╝██║████╗  ██║██╔════╝ ██║   ██║██║     ██╔══██╗██╔══██╗██║██╔════╝   ║
║   ███████╗██║██╔██╗ ██║██║  ███╗██║   ██║██║     ███████║██████╔╝██║███████╗   ║
║   ╚════██║██║██║╚██╗██║██║   ██║██║   ██║██║     ██╔══██║██╔══██╗██║╚════██║   ║
║   ███████║██║██║ ╚████║╚██████╔╝╚██████╔╝███████╗██║  ██║██║  ██║██║███████║   ║
║   ╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝   ║
║                                                                  ║
║                         BETA v2.4 CLOUD                          ║
║              "One Being, Striving for Coherence"                 ║
║         HaackLang + SCCE • Cloud-Only • Research                 ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

    Architecture:  BeingState + CoherenceEngine + HaackLang + SCCE
    Philosophy:    Spinoza → IIT → Lumen → Buddhism
    Mathematics:   C: B → [0,1], max E[C(B(t+1))]
    Cognition:     Polyrhythmic Tracks + Temporal Dynamics
    Integration:   50+ Subsystems → 1 Unified Being
    Cloud:         Gemini 2.5 Flash + Claude 3.5 Haiku + GPT-5
    Research:      Perplexity AI (Skyrim best practices)
    MetaCognition: OpenRouter (GPT-4o + DeepSeek planning)
    
"""
    print(banner)


def check_environment():
    """Check that required environment variables are set."""
    required_vars = {
        'OPENAI_API_KEY': 'OpenAI API (required for GPT-5 orchestrator)',
        'GEMINI_API_KEY': 'Google Gemini API (required for vision)',
    }
    
    optional_vars = {
        'ANTHROPIC_API_KEY': 'Anthropic Claude API (optional)',
        'PERPLEXITY_API_KEY': 'Perplexity AI (optional - for research advisor)',
        'OPENROUTER_API_KEY': 'OpenRouter (optional - for metacognition)',
        'GITHUB_TOKEN': 'GitHub Token (optional - fallback for OpenRouter)',
        'HYPERBOLIC_API_KEY': 'Hyperbolic API (optional - for Qwen3-235B)',
    }
    
    missing_required = []
    missing_optional = []
    
    print("\n[ENV] Checking environment variables...")
    
    for var, description in required_vars.items():
        if os.getenv(var):
            print(f"  [OK] {var}: Set")
        else:
            print(f"  [X] {var}: Missing ({description})")
            missing_required.append(var)
    
    for var, description in optional_vars.items():
        if os.getenv(var):
            print(f"  [OK] {var}: Set")
        else:
            print(f"  [-] {var}: Not set ({description})")
            missing_optional.append(var)
    
    if missing_required:
        print(f"\n[ERROR] Missing required environment variables: {', '.join(missing_required)}")
        print("\nPlease set them in your .env file or export them:")
        for var in missing_required:
            print(f"  export {var}='your-key-here'")
        return False
    
    if missing_optional:
        print(f"\n[INFO] Optional features disabled: {', '.join(missing_optional)}")
    
    print("\n[ENV] [OK] Environment check passed\n")
    return True


def load_config(args) -> 'SkyrimConfig':
    """Load and configure the system."""
    from singularis.skyrim.skyrim_agi import SkyrimConfig
    
    print("[CONFIG] Loading configuration...")
    print("[CONFIG] Mode: CLOUD-ONLY with HaackLang + SCCE")
    
    config = SkyrimConfig()
    
    # ========================================
    # HaackLang + SCCE Configuration (NEW)
    # ========================================
    config.use_haacklang = True
    config.haack_beat_interval = 0.1  # 10 Hz
    config.haack_verbose = args.verbose
    config.scce_profile = args.profile
    config.scce_frequency = 1  # Every cycle
    
    # ========================================
    # Cloud-Only: Disable Local LLMs
    # ========================================
    config.use_local_fallback = False  # No local LLMs
    config.enable_legacy_llms = False  # No legacy models
    
    # Force cloud models
    config.use_hybrid_llm = True  # Gemini + Claude
    config.use_gemini_vision = True
    config.use_claude_reasoning = True
    
    # Parallel mode: Run MoE and Hybrid together
    config.use_parallel_mode = True
    
    # ========================================
    # Command-line Overrides
    # ========================================
    if args.cycle_interval:
        config.cycle_interval = args.cycle_interval
    
    if args.no_voice:
        config.enable_voice = False
    
    if args.no_video:
        config.enable_video_interpreter = False
    
    # Performance settings
    if args.fast:
        print("  [FAST MODE] Optimizing for speed...")
        config.cycle_interval = 1.0
        config.enable_voice = False
        config.enable_video_interpreter = False
        config.gpt5_verbose = False
        config.haack_verbose = False
    
    # Safety settings
    if args.conservative:
        print("  [CONSERVATIVE MODE] Reducing API calls...")
        config.cycle_interval = 5.0
        config.gemini_rpm_limit = 10
        config.num_gemini_experts = 1
        config.num_claude_experts = 1
        config.scce_frequency = 5  # Only every 5th cycle
    
    print(f"\n  [HaackLang] Enabled: True")
    print(f"  [HaackLang] Beat interval: {config.haack_beat_interval}s (10 Hz)")
    print(f"  [HaackLang] Verbose: {config.haack_verbose}")
    print(f"  [SCCE] Profile: {config.scce_profile}")
    print(f"  [SCCE] Frequency: Every {config.scce_frequency} cycle(s)")
    print(f"\n  [Cloud] Gemini Vision: Enabled")
    print(f"  [Cloud] Claude Reasoning: Enabled")
    print(f"  [Cloud] Local LLMs: DISABLED")
    print(f"\n  Cycle interval: {config.cycle_interval}s")
    print(f"  Voice enabled: {config.enable_voice}")
    print(f"  Video enabled: {config.enable_video_interpreter}")
    print(f"  GPT-5 orchestrator: {config.use_gpt5_orchestrator}")
    print(f"  Double Helix: {config.use_double_helix}")
    print(f"  Verbose mode: {config.gpt5_verbose}")
    print(f"  Research Advisor: {'Enabled' if os.getenv('PERPLEXITY_API_KEY') else 'Disabled (no API key)'}")
    print(f"  MetaCognition: {'Enabled' if (os.getenv('OPENROUTER_API_KEY') or os.getenv('GITHUB_TOKEN')) else 'Disabled (no API key)'}")
    
    print("\n[CONFIG] [OK] Configuration loaded\n")
    return config


async def run_async_mode(duration: int, config: 'SkyrimConfig'):
    """Run in asynchronous mode (recommended)."""
    from singularis.skyrim.skyrim_agi import SkyrimAGI
    
    print("=" * 70)
    print("ASYNC MODE - Full Parallel Processing")
    print("=" * 70)
    print(f"Duration: {duration} seconds ({duration // 60} minutes)")
    print(f"Mode: Asynchronous (perception || reasoning || action)")
    print(f"Cognition: HaackLang + SCCE")
    print(f"Profile: {config.scce_profile}")
    print("=" * 70 + "\n")
    
    # Initialize AGI
    print("[INIT] Initializing Singularis AGI...\n")
    agi = SkyrimAGI(config)
    
    # Initialize LLM systems
    print("[INIT] Initializing cloud LLM systems...\n")
    await agi.initialize_llm()
    
    # Verify core systems
    if not hasattr(agi, 'being_state'):
        print("[ERROR] BeingState not initialized!")
        return
    
    if not hasattr(agi, 'coherence_engine'):
        print("[ERROR] CoherenceEngine not initialized!")
        return
    
    print("[VERIFY] [OK] BeingState initialized")
    print("[VERIFY] [OK] CoherenceEngine initialized")
    print("[VERIFY] [OK] Metaphysical center operational")
    
    # Verify HaackLang + SCCE
    if hasattr(agi, 'haack_bridge') and agi.haack_bridge:
        print(f"[VERIFY] [OK] HaackLang runtime initialized")
        print(f"[VERIFY] [OK] SCCE profile: {agi.scce_profile.name}")
        print(f"[VERIFY] [OK] Temporal cognitive dynamics enabled")
    else:
        print("[WARNING] HaackLang/SCCE not initialized")
    
    # Verify cloud systems
    if hasattr(agi, 'hybrid_llm') and agi.hybrid_llm:
        print(f"[VERIFY] [OK] Hybrid LLM (Gemini + Claude) initialized")
    else:
        print("[WARNING] Hybrid LLM not initialized")
    
    # Verify advisory systems
    if hasattr(agi, 'research_advisor'):
        if agi.research_advisor.client.is_available():
            print("[VERIFY] [OK] Research Advisor (Perplexity) initialized")
        else:
            print("[VERIFY] [-] Research Advisor disabled (no PERPLEXITY_API_KEY)")
    
    if hasattr(agi, 'metacog_advisor'):
        if agi.metacog_advisor.client.is_available():
            print("[VERIFY] [OK] MetaCognition Advisor (OpenRouter) initialized")
        else:
            print("[VERIFY] [-] MetaCognition Advisor disabled (no OPENROUTER_API_KEY)")
    
    if hasattr(agi, 'gpt5_orchestrator') and agi.gpt5_orchestrator:
        num_systems = len(agi.gpt5_orchestrator.registered_systems)
        print(f"[VERIFY] [OK] GPT-5 Orchestrator initialized ({num_systems} systems registered)")
    
    if hasattr(agi, 'double_helix') and agi.double_helix:
        helix_stats = agi.double_helix.get_stats()
        print(f"[VERIFY] [OK] Double Helix initialized ({helix_stats.get('total_nodes', 0)} nodes)")
    
    if hasattr(agi, 'main_brain') and agi.main_brain:
        print(f"[VERIFY] [OK] Main Brain initialized (session: {agi.main_brain.session_id})")
    
    print()
    
    # Start autonomous play
    print("[START] Beginning autonomous gameplay...\n")
    print("=" * 70)
    print("THE ONE BEING IS NOW STRIVING FOR COHERENCE")
    print("WITH POLYRHYTHMIC COGNITION")
    print("=" * 70 + "\n")
    
    try:
        await agi.autonomous_play(duration_seconds=duration)
    except KeyboardInterrupt:
        print("\n\n[INTERRUPT] Received keyboard interrupt, shutting down gracefully...")
    except Exception as e:
        print(f"\n\n[ERROR] Fatal error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Print final statistics
        print("\n" + "=" * 70)
        print("SESSION COMPLETE")
        print("=" * 70)
        
        if hasattr(agi, 'being_state'):
            print(f"\nFinal BeingState:")
            print(f"  Cycle: {agi.being_state.cycle_number}")
            print(f"  C_global: {agi.being_state.global_coherence:.3f}")
            
            if agi.being_state.lumina:
                balance = agi.being_state.lumina.balance_score()
                print(f"  Lumina: (ontic={agi.being_state.lumina.ontic:.3f}, "
                      f"structural={agi.being_state.lumina.structural:.3f}, "
                      f"participatory={agi.being_state.lumina.participatory:.3f})")
                print(f"  Lumina Balance: {balance:.3f}")
            
            print(f"  Consciousness: C={agi.being_state.coherence_C:.3f}, Phi={agi.being_state.phi_hat:.3f}")
            print(f"  Temporal Coherence: {agi.being_state.temporal_coherence:.3f}")
            print(f"  Emotion: {agi.being_state.primary_emotion} (intensity={agi.being_state.emotion_intensity:.2f})")
            print(f"  Spiral Stage: {agi.being_state.spiral_stage}")
            print(f"  Goal: {agi.being_state.current_goal}")
            print(f"  Last Action: {agi.being_state.last_action}")
        
        # HaackLang + SCCE stats
        if hasattr(agi, 'haack_bridge') and agi.haack_bridge:
            print(f"\nHaackLang + SCCE Statistics:")
            try:
                danger_tv = agi.haack_bridge.get_truthvalue('danger')
                fear_tv = agi.haack_bridge.get_truthvalue('fear')
                trust_tv = agi.haack_bridge.get_truthvalue('trust')
                
                if danger_tv:
                    print(f"  Danger: P={danger_tv.get('perception'):.2f} S={danger_tv.get('strategic'):.2f} I={danger_tv.get('intuition'):.2f}")
                if fear_tv:
                    print(f"  Fear:   P={fear_tv.get('perception'):.2f} S={fear_tv.get('strategic'):.2f} I={fear_tv.get('intuition'):.2f}")
                if trust_tv:
                    print(f"  Trust:  P={trust_tv.get('perception'):.2f} S={trust_tv.get('strategic'):.2f} I={trust_tv.get('intuition'):.2f}")
                print(f"  Profile: {agi.scce_profile.name}")
                print(f"  Global Beat: {agi.haack_bridge.runtime.scheduler.global_beat}")
            except Exception as e:
                print(f"  [Error getting HaackLang stats: {e}]")
        
        if hasattr(agi, 'coherence_engine'):
            stats = agi.coherence_engine.get_stats()
            print(f"\nCoherence Statistics:")
            print(f"  Mean: {stats.get('mean', 0):.3f}")
            print(f"  Std: {stats.get('std', 0):.3f}")
            print(f"  Min: {stats.get('min', 0):.3f}")
            print(f"  Max: {stats.get('max', 0):.3f}")
            print(f"  Trend: {stats.get('trend', 'unknown')}")
        
        if hasattr(agi, 'stats'):
            print(f"\nPerformance:")
            print(f"  Cycles: {agi.stats.get('cycles_completed', 0)}")
            print(f"  Actions: {agi.stats.get('actions_taken', 0)}")
            print(f"  Success Rate: {agi.stats.get('action_success_rate', 0):.1%}")
        
        print("\n" + "=" * 70)
        print("Thank you for using Singularis Beta v2.4 Cloud")
        print("=" * 70 + "\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Singularis Beta v2.4 - Cloud Runtime with HaackLang + SCCE',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run for 1 hour with balanced profile (default)
  python run_beta_v2.4_cloud.py --duration 3600
  
  # Run with anxious profile (emotions linger)
  python run_beta_v2.4_cloud.py --duration 3600 --profile anxious
  
  # Run with stoic profile (fast emotional recovery)
  python run_beta_v2.4_cloud.py --duration 3600 --profile stoic
  
  # Run in fast mode (no voice/video)
  python run_beta_v2.4_cloud.py --duration 1800 --fast
  
  # Run in conservative mode (fewer API calls)
  python run_beta_v2.4_cloud.py --duration 3600 --conservative
  
  # Run with custom cycle interval
  python run_beta_v2.4_cloud.py --duration 1800 --cycle-interval 2.5

Philosophy:
  Singularis v2.4 implements "one being striving for coherence" through:
  - BeingState: The unified state of being
  - CoherenceEngine: The measurement of "how well the being is being"
  - HaackLang: Polyrhythmic cognitive execution (tracks: perception, strategic, intuition)
  - SCCE: Temporal cognitive dynamics (fear, trust, stress, curiosity evolution)
  - C_global: The one thing all subsystems optimize
  
  This is Spinoza's conatus made executable with temporal awareness.

Profiles:
  - balanced: Default balanced regulation
  - anxious: Emotions linger, prone to panic
  - stoic: Fast recovery, maintains composure
  - curious: Low stress, high novelty response
  - aggressive: Fast reactions, impulsive
  - cautious: Slow to act, risk averse
        """
    )
    
    parser.add_argument(
        '--duration',
        type=int,
        default=1800,
        help='Duration in seconds (default: 1800 = 30 minutes)'
    )
    
    # HaackLang + SCCE options
    parser.add_argument(
        '--profile',
        choices=['balanced', 'anxious', 'stoic', 'curious', 'aggressive', 'cautious'],
        default='balanced',
        help='SCCE personality profile (default: balanced)'
    )
    
    # Performance options
    parser.add_argument(
        '--cycle-interval',
        type=float,
        help='Override cycle interval in seconds (default from config)'
    )
    
    parser.add_argument(
        '--fast',
        action='store_true',
        help='Fast mode: disable voice, video for speed'
    )
    
    parser.add_argument(
        '--conservative',
        action='store_true',
        help='Conservative mode: reduce API calls, increase intervals'
    )
    
    # Feature toggles
    parser.add_argument(
        '--no-voice',
        action='store_true',
        help='Disable voice system'
    )
    
    parser.add_argument(
        '--no-video',
        action='store_true',
        help='Disable video interpreter'
    )
    
    # Debug options
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output (includes HaackLang logging)'
    )
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Load configuration
    config = load_config(args)
    
    # Run
    try:
        asyncio.run(run_async_mode(args.duration, config))
    except Exception as e:
        print(f"\n[FATAL] Unhandled exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
