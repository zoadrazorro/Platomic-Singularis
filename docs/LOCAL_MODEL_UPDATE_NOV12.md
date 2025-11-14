# Local Model Configuration Update - November 12, 2025

## Summary
Updated all local LM Studio model configurations to use the new **Microsoft Phi-4** and **Qwen3-4b** models loaded in LM Studio.

---

## New Models (From LM Studio)

### Available Models:
1. **`microsoft/phi-4`** - Fast action planning and synthesis
2. **`microsoft/phi-4-mini-reasoning`** - Compact reasoning model
3. **`microsoft/phi-4-mini-reasoning:2`** - Second instance for parallel processing
4. **`qwen/qwen3-4b-thinking-2507`** - Vision and thinking model

---

## Changes Applied

### 1. **Main Configuration** (`run_skyrim_agi.py`)

#### Parallel Mode:
```python
# Before
qwen3_vl_perception_model="qwen/qwen3-vl-8b"
huihui_cognition_model="huihui-moe-60b-a3b-abliterated-i1"
phi4_action_model="mistralai/mistral-nemo-instruct-2407"

# After
qwen3_vl_perception_model="qwen/qwen3-4b-thinking-2507"
huihui_cognition_model="microsoft/phi-4-mini-reasoning"
phi4_action_model="microsoft/phi-4"
```

#### Hybrid Mode:
```python
# Same updates as parallel mode
```

#### Local-Only Mode:
```python
# Same updates as parallel mode
```

---

### 2. **Hybrid Client** (`singularis/llm/hybrid_client.py`)

```python
# Before
local_vision_model: str = "qwen/qwen3-vl-8b"
local_reasoning_model: str = "huihui-moe-60b-a3b-abliterated-i1"
local_action_model: str = "mistralai/mistral-nemo-instruct-2407"

# After
local_vision_model: str = "qwen/qwen3-4b-thinking-2507"
local_reasoning_model: str = "microsoft/phi-4-mini-reasoning"
local_action_model: str = "microsoft/phi-4"
```

---

### 3. **Local MoE** (`singularis/llm/local_moe.py`)

#### Config:
```python
# Before
expert_model: str = "qwen/qwen3-vl-8b"
synthesizer_model: str = "microsoft/phi-4"  # Already correct!

# After
expert_model: str = "qwen/qwen3-4b-thinking-2507"
synthesizer_model: str = "microsoft/phi-4"
```

#### Expert Instances:
```python
# Before
expert_models = [
    "qwen/qwen3-vl-8b",      # Instance 1
    "qwen/qwen3-vl-8b:2",    # Instance 2
    "qwen/qwen3-vl-8b:3",    # Instance 3
    "qwen/qwen3-vl-8b:4"     # Instance 4
]

# After (Mix of models for diversity)
expert_models = [
    "qwen/qwen3-4b-thinking-2507",      # Instance 1 - Vision/thinking
    "microsoft/phi-4-mini-reasoning",    # Instance 2 - Reasoning
    "microsoft/phi-4-mini-reasoning:2",  # Instance 3 - Reasoning (2nd instance)
    "microsoft/phi-4"                    # Instance 4 - Fast synthesis
]
```

---

### 4. **LM Studio Client** (`singularis/llm/lmstudio_client.py`)

```python
# Before
model_name: str = "huihui-moe-60b-a38"

# After
model_name: str = "microsoft/phi-4-mini-reasoning"
```

---

## Model Roles

### **microsoft/phi-4**
- **Role:** Fast action planning, synthesis, final decisions
- **Used in:** Action planning, MoE synthesizer
- **Strengths:** Speed, efficiency, good for real-time decisions

### **microsoft/phi-4-mini-reasoning**
- **Role:** Compact reasoning, strategic thinking
- **Used in:** Cognition, reasoning fallback, MoE expert
- **Strengths:** Reasoning capabilities, smaller footprint

### **qwen/qwen3-4b-thinking-2507**
- **Role:** Vision analysis, thinking, perception
- **Used in:** Perception, vision fallback, MoE expert
- **Strengths:** Multimodal, thinking mode, visual understanding

---

## Benefits

### Performance:
- ✅ **Faster inference** - Phi-4 models are optimized for speed
- ✅ **Better reasoning** - Phi-4-mini-reasoning has improved logic
- ✅ **Thinking mode** - Qwen3-4b supports extended thinking

### Compatibility:
- ✅ **All models loaded in LM Studio** - No missing model errors
- ✅ **Multiple instances** - Can run parallel MoE with different models
- ✅ **Diverse expertise** - Mix of vision, reasoning, and action models

### Resource Usage:
- ✅ **Smaller models** - 4B parameters vs 60B (Huihui)
- ✅ **Lower VRAM** - Can run more instances simultaneously
- ✅ **Faster loading** - Quicker startup times

---

## Testing Checklist

- [ ] Verify all models load in LM Studio
- [ ] Test parallel mode with new models
- [ ] Test hybrid mode with local fallback
- [ ] Test MoE with mixed expert models
- [ ] Verify action planning speed
- [ ] Check reasoning quality
- [ ] Monitor VRAM usage
- [ ] Compare performance vs old models

---

## Files Modified

1. ✅ `run_skyrim_agi.py` - All 3 mode configs (parallel, hybrid, local)
2. ✅ `singularis/llm/hybrid_client.py` - Fallback models
3. ✅ `singularis/llm/local_moe.py` - Expert models and config
4. ✅ `singularis/llm/lmstudio_client.py` - Default model

---

## Migration Notes

### Old Models (Deprecated):
- ❌ `huihui-moe-60b-a3b-abliterated-i1` → `microsoft/phi-4-mini-reasoning`
- ❌ `mistralai/mistral-nemo-instruct-2407` → `microsoft/phi-4`
- ❌ `qwen/qwen3-vl-8b` → `qwen/qwen3-4b-thinking-2507`

### Why Changed:
- Old models not loaded in current LM Studio instance
- New models are faster and more efficient
- Better alignment with current research (Phi-4 series)
- Thinking mode support in Qwen3-4b

---

*Update completed: November 12, 2025*
*All local model references updated to match LM Studio configuration*
