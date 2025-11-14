# Singularis Beta v2.4 Cloud Runtime

**Version**: 2.4.0-beta  
**Date**: November 14, 2025  
**Status**: Production-Ready

---

## What's New in v2.4

### 🎵 **HaackLang + SCCE Integration**
- **Polyrhythmic cognitive execution** (3 tracks: perception, strategic, intuition)
- **Temporal cognitive dynamics** (fear, trust, stress, curiosity evolution)
- **6 personality profiles** (balanced, anxious, stoic, curious, aggressive, cautious)
- **Paraconsistent logic** (handle contradictions without explosion)
- **Meta-logic operators** (@coh, @conflict, @resolve)

### ☁️ **Cloud-Only Mode**
- **No local LLMs** - relies entirely on cloud APIs
- **Gemini 2.5 Flash** for vision
- **Claude 3.5 Haiku** for reasoning
- **GPT-5** for orchestration
- **Optimized for performance** - no local model overhead

---

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set API Keys
Create a `.env` file:
```bash
OPENAI_API_KEY=your-openai-key-here
GEMINI_API_KEY=your-gemini-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here  # Optional
PERPLEXITY_API_KEY=your-perplexity-key-here  # Optional
OPENROUTER_API_KEY=your-openrouter-key-here  # Optional
```

### 3. Run with Default Settings
```bash
python run_beta_v2.4_cloud.py --duration 3600
```

This will run for 1 hour (3600 seconds) with:
- **Profile**: Balanced (default)
- **Cycle interval**: 3.0s
- **Voice**: Enabled
- **Video**: Enabled
- **HaackLang**: Enabled
- **SCCE**: Every cycle

---

## Personality Profiles

Choose a profile with `--profile <name>`:

### **balanced** (Default)
```bash
python run_beta_v2.4_cloud.py --duration 3600 --profile balanced
```
- Moderate emotional regulation
- Balanced risk/reward
- Good for general gameplay

### **anxious**
```bash
python run_beta_v2.4_cloud.py --duration 3600 --profile anxious
```
- Emotions linger longer
- Prone to panic under stress
- Quick to flee from danger
- **Use for**: Survival horror, permadeath runs

### **stoic**
```bash
python run_beta_v2.4_cloud.py --duration 3600 --profile stoic
```
- Fast emotional recovery
- Maintains composure under pressure
- Slow to panic
- **Use for**: Boss fights, high-stress combat

### **curious**
```bash
python run_beta_v2.4_cloud.py --duration 3600 --profile curious
```
- Low stress accumulation
- High novelty response
- Explores more, fights less
- **Use for**: Exploration, discovery

### **aggressive**
```bash
python run_beta_v2.4_cloud.py --duration 3600 --profile aggressive
```
- Fast reactions
- Impulsive decision-making
- Prefers combat over retreat
- **Use for**: Power fantasy, combat-focused gameplay

### **cautious**
```bash
python run_beta_v2.4_cloud.py --duration 3600 --profile cautious
```
- Slow to act
- Risk averse
- Prefers safe, tested approaches
- **Use for**: New areas, dangerous encounters

---

## Performance Modes

### Fast Mode
```bash
python run_beta_v2.4_cloud.py --duration 1800 --fast
```
- Cycle interval: 1.0s
- Voice: Disabled
- Video: Disabled
- Verbose: Disabled
- **Best for**: Testing, quick runs

### Conservative Mode
```bash
python run_beta_v2.4_cloud.py --duration 3600 --conservative
```
- Cycle interval: 5.0s
- Reduced API calls
- SCCE: Every 5th cycle
- **Best for**: Limited API quotas, overnight runs

### Custom Cycle Interval
```bash
python run_beta_v2.4_cloud.py --duration 3600 --cycle-interval 2.5
```
- Override default cycle time
- **Best for**: Fine-tuning performance

---

## Feature Toggles

### Disable Voice
```bash
python run_beta_v2.4_cloud.py --duration 3600 --no-voice
```

### Disable Video
```bash
python run_beta_v2.4_cloud.py --duration 3600 --no-video
```

### Verbose Mode (Debug)
```bash
python run_beta_v2.4_cloud.py --duration 3600 --verbose
```
Enables:
- HaackLang guard logging
- SCCE evolution details
- GPT-5 orchestrator messages

---

## Example Commands

### 1-Hour Exploration (Curious)
```bash
python run_beta_v2.4_cloud.py --duration 3600 --profile curious
```

### 30-Minute Boss Fight (Stoic)
```bash
python run_beta_v2.4_cloud.py --duration 1800 --profile stoic --no-video
```

### Overnight Run (Conservative + Cautious)
```bash
python run_beta_v2.4_cloud.py --duration 28800 --profile cautious --conservative
```

### Fast Testing (5 minutes)
```bash
python run_beta_v2.4_cloud.py --duration 300 --fast --verbose
```

---

## Console Output

### During Initialization
```
[23/28] HaackLang + SCCE integration...
  [OK] HaackLang runtime initialized
  [OK] Loaded 3 cognitive modules:
      - danger_evaluation.haack
      - action_selection.haack
      - coherence_monitoring.haack
  [OK] Registered 8 Python callbacks
  [OK] SCCE profile: Balanced
  [OK] Temporal cognitive dynamics enabled
```

### During Gameplay (Every 10 Cycles)
```
[SCCE] Coherence: 0.723 | Profile: Balanced
[SCCE]   Danger: P=0.65 S=0.48 I=0.32
[SCCE]   Fear:   P=0.42 S=0.35 I=0.28
[SCCE]   Trust:  P=0.75 S=0.72 I=0.68
[SCCE]   Stress: P=0.38 S=0.35 I=0.30
```

### When Guards Fire
```
[HAACK] Guard triggered: execute_flee
[HAACK] Action executed: FLEE
```

---

## Architecture

### Data Flow
```
Perception (Singularis)
    ↓
TruthValue Sync (Python → HaackLang)
    ↓
SCCE Cognition Step (temporal dynamics)
    ↓
HaackLang Runtime (tracks, contexts, guards)
    ↓
Actions (HaackLang → Python)
    ↓
Game Execution
```

### Cognitive Tracks
```
Perception Track (1 beat):   Fast, immediate responses
Strategic Track (3 beats):    Slower, deliberate planning
Intuition Track (7 beats):    Subconscious, emergent insights
```

### SCCE Primitives
- **Decay**: Emotions fade over time
- **Reinforce**: Repetition strengthens beliefs
- **Propagate**: Perception → Strategic → Intuition
- **Inhibit**: Trust inhibits fear
- **Amplify**: Danger amplifies stress
- **Interference**: Rhythmic spikes → emergent behavior

---

## Comparison with v2.3

| Feature | v2.3 | v2.4 Cloud |
|---------|------|------------|
| BeingState | ✅ | ✅ |
| CoherenceEngine | ✅ | ✅ |
| HaackLang | ❌ | ✅ |
| SCCE | ❌ | ✅ |
| Personality Profiles | ❌ | ✅ (6 profiles) |
| Local LLMs | ✅ | ❌ (cloud-only) |
| Temporal Dynamics | ❌ | ✅ |
| Polyrhythmic Cognition | ❌ | ✅ (3 tracks) |

---

## Performance

### Overhead
- **SCCE cognition_step**: < 1ms per cycle
- **HaackLang runtime**: < 0.5ms per cycle
- **Total overhead**: < 1.5ms (~0.5% of 3s cycle)

### API Calls (Default Config)
- **Gemini**: ~15 calls/min (well under 30 RPM limit)
- **Claude**: ~10 calls/min (well under 100 RPM limit)
- **GPT-5**: ~5 calls/min (orchestration only)

---

## Troubleshooting

### "Missing required environment variables"
- Ensure `.env` file exists
- Check `OPENAI_API_KEY` and `GEMINI_API_KEY` are set

### "HaackLang/SCCE initialization failed"
- Check `singularis/skyrim/Haacklang/` directory exists
- Verify cognitive modules are present in `cognitive_modules/`
- Try with `--verbose` to see detailed error

### API Rate Limits
- Use `--conservative` mode
- Increase `--cycle-interval`
- Reduce expert counts in config

### Performance Issues
- Use `--fast` mode
- Disable voice/video with `--no-voice --no-video`
- Increase cycle interval to 4-5 seconds

---

## Files

| File | Purpose |
|------|---------|
| `run_beta_v2.4_cloud.py` | Main runtime script |
| `BETA_V2.4_CLOUD_README.md` | This file |
| `HAACK_SCCE_INTEGRATION_COMPLETE.md` | Integration details |
| `test_haack_scce_integration.py` | Dry-run test |

---

## Next Steps

1. **Test with dry run first**:
   ```bash
   python test_haack_scce_integration.py
   ```

2. **Run short session** (5 minutes):
   ```bash
   python run_beta_v2.4_cloud.py --duration 300 --fast
   ```

3. **Try different profiles**:
   ```bash
   python run_beta_v2.4_cloud.py --duration 600 --profile anxious
   python run_beta_v2.4_cloud.py --duration 600 --profile stoic
   python run_beta_v2.4_cloud.py --duration 600 --profile curious
   ```

4. **Full production run** (1 hour):
   ```bash
   python run_beta_v2.4_cloud.py --duration 3600 --profile balanced
   ```

---

## Documentation

- **Integration Guide**: `HAACKLANG_INTEGRATION_GUIDE.md`
- **SCCE Guide**: `singularis/skyrim/Haacklang/docs/SCCE_IMPLEMENTATION_GUIDE.md`
- **HLVM Phase 1**: `HLVM_PHASE1_COMPLETE.md`
- **SCCE Complete**: `SCCE_COMPLETE.md`
- **Integration Summary**: `HAACK_SCCE_INTEGRATION_COMPLETE.md`

---

## Support

For issues, questions, or feedback:
1. Check the documentation files listed above
2. Review console output with `--verbose` flag
3. Run dry-run test: `python test_haack_scce_integration.py`

---

**Singularis Beta v2.4 Cloud** - The math layer of the mind, now with temporal awareness. 🎵
