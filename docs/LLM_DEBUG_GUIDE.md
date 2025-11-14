# LLM Debugging Guide

## What to Look For When Running

When you run the Skyrim AGI with LLM enabled, you should see these debug messages:

### 1. At Initialization
```
Initializing LLM consciousness engine...
[LLM] ✓ LLM consciousness engine initialized successfully
[LLM] Type: <class 'singularis.consciousness.meta_orchestrator_llm.MetaOrchestratorLLM'>
```

**If you see this instead:**
```
[LLM] ⚠️ LLM consciousness engine is None - will use heuristic planning only
```
Then the LLM failed to initialize. Check:
- Is LM Studio running?
- Is the model loaded in LM Studio?
- Is the server URL correct (default: http://localhost:1234)?

### 2. During Planning (Each Cycle)
```
[DEBUG] LLM Check: hasattr=True, consciousness_llm=<MetaOrchestratorLLM object>
[PLANNING] Using LLM-based strategic planning...
[LLM] Calling LM Studio for layer-aware action planning...
[LLM] Context length: XXX characters
[LLM] Result type: <class 'dict'>
[LLM] Result keys: dict_keys(['consciousness_response', ...])
[LLM] Raw response: explore
[LLM] Response length: 7 characters
[LLM] Selected action: explore
```

**If you see this instead:**
```
[DEBUG] LLM Check: hasattr=True, consciousness_llm=None
[PLANNING] LLM not available, using heuristic planning...
```
Then the LLM is not initialized even though the attribute exists.

**If you see:**
```
[PLANNING] Using LLM-based strategic planning...
[LLM] Planning failed: <error message>
```
Then the LLM call is failing. Common issues:
- LM Studio server not responding
- Model not loaded
- Network/connection issue
- Timeout

## Common Issues

### Issue: LLM Not Initialized
**Symptoms:** `consciousness_llm=None`
**Solutions:**
1. Make sure you answered 'Y' to "Use LLM for smarter decisions?"
2. Check LM Studio is running and has a model loaded
3. Check the initialization error message in the output

### Issue: LLM Calls Failing
**Symptoms:** "Planning failed" messages
**Solutions:**
1. Check LM Studio server is responding (visit http://localhost:1234 in browser)
2. Check model is loaded and ready
3. Look at the full error traceback for details

### Issue: Using Heuristics Instead of LLM
**Symptoms:** Always seeing "using heuristic planning"
**Solutions:**
1. Check the debug output shows `hasattr=True` and `consciousness_llm` is not None
2. If consciousness_llm is None, the initialization failed
3. Re-run with LLM enabled and watch for initialization errors

## Testing LLM Connection

Before running the full AGI, you can test if LM Studio is working:

```python
import asyncio
from singularis.skyrim import SkyrimAGI, SkyrimConfig

async def test():
    config = SkyrimConfig(dry_run=True)
    agi = SkyrimAGI(config)
    await agi.initialize_llm()
    
asyncio.run(test())
```

You should see the success message if everything is working.
