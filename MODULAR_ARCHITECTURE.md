# Modular Architecture Guide 🧩

**How to structure Singularis for independent module deployment**

---

## Overview

The Singularis repository is being restructured into independent, loosely-coupled modules that can be:
- Cloned into separate repositories
- Deployed independently
- Versioned separately
- Mixed and matched as needed

---

## Module Structure

### Core Modules (Independent Repos)

```
singularis/
├── singularis-core/          # Core AGI consciousness
├── singularis-lifeops/       # Life Operations & Timeline
├── singularis-perception/    # Vision & Audio processing
├── singularis-integrations/  # External service adapters
├── singularis-skyrim/        # Skyrim AGI environment
└── singularis-deployment/    # Deployment configs & docs
```

---

## Module Definitions

### 1. `singularis-core` 🧠
**Purpose**: Core AGI consciousness and reasoning

**Contains**:
```
singularis-core/
├── singularis/
│   ├── consciousness/
│   │   ├── unified_consciousness_layer.py
│   │   ├── voice_system.py
│   │   ├── enhanced_coherence.py
│   │   └── lumen_integration.py
│   ├── llm/
│   │   ├── gpt5_orchestrator.py
│   │   ├── moe_orchestrator.py
│   │   ├── async_expert_pool.py
│   │   └── model_router.py
│   ├── core/
│   │   ├── temporal_binding.py
│   │   ├── being_state.py
│   │   └── double_helix.py
│   └── learning/
│       ├── continual_learner.py
│       └── hierarchical_memory.py
├── tests/
├── requirements.txt
├── setup.py
└── README.md
```

**Dependencies**:
- PyTorch
- Transformers
- OpenAI SDK
- Google Generative AI
- Loguru

**API Surface**:
```python
from singularis.consciousness import UnifiedConsciousnessLayer
from singularis.core import BeingState, TemporalBinding
from singularis.llm import GPT5Orchestrator

# Initialize
consciousness = UnifiedConsciousnessLayer()
result = await consciousness.process_unified(query, context)
```

**Independent**: ✅ Yes - No external module dependencies

---

### 2. `singularis-lifeops` 📊
**Purpose**: Life Timeline, patterns, interventions, queries

**Contains**:
```
singularis-lifeops/
├── lifeops/
│   ├── life_timeline.py
│   ├── pattern_engine.py
│   ├── intervention_policy.py
│   ├── emergency_validator.py
│   └── life_ops/
│       ├── life_timeline_bridge.py
│       ├── agi_pattern_arbiter.py
│       ├── agi_intervention_decider.py
│       └── life_query_handler.py
├── tests/
├── requirements.txt
├── setup.py
└── README.md
```

**Dependencies**:
- SQLite/PostgreSQL
- Pandas
- NumPy
- Scikit-learn

**External Module Dependencies**:
- `singularis-core` (for consciousness integration)

**API Surface**:
```python
from lifeops import LifeTimeline, PatternEngine
from lifeops.life_ops import LifeQueryHandler

# Initialize
timeline = LifeTimeline("data/timeline.db")
query_handler = LifeQueryHandler(consciousness, timeline)
result = await query_handler.handle_query(user_id, query)
```

**Independent**: ⚠️ Partial - Requires `singularis-core` for AGI features

---

### 3. `singularis-perception` 👁️
**Purpose**: Vision, audio, and multimodal processing

**Contains**:
```
singularis-perception/
├── perception/
│   ├── streaming_video_interpreter.py
│   ├── vision_processor.py
│   ├── audio_processor.py
│   └── multimodal_fusion.py
├── tests/
├── requirements.txt
├── setup.py
└── README.md
```

**Dependencies**:
- OpenCV (cv2)
- PIL/Pillow
- Google Generative AI (Gemini)
- PyTorch
- Transformers

**External Module Dependencies**:
- None (standalone)

**API Surface**:
```python
from perception import StreamingVideoInterpreter

# Initialize
interpreter = StreamingVideoInterpreter(mode="comprehensive")
analysis = await interpreter.analyze_frame(frame)
```

**Independent**: ✅ Yes - Fully standalone

---

### 4. `singularis-integrations` 🔌
**Purpose**: External service adapters (Messenger, Fitbit, cameras, etc.)

**Contains**:
```
singularis-integrations/
├── integrations/
│   ├── messenger_bot_adapter.py
│   ├── fitbit_health_adapter.py
│   ├── meta_glasses_adapter.py
│   ├── roku_screencap_gateway.py
│   └── main_orchestrator.py
├── tests/
├── requirements.txt
├── setup.py
└── README.md
```

**Dependencies**:
- FastAPI
- aiohttp
- requests
- ADB tools

**External Module Dependencies**:
- `singularis-core` (consciousness)
- `singularis-lifeops` (timeline)
- `singularis-perception` (vision)

**API Surface**:
```python
from integrations import MainOrchestrator

# Initialize
orchestrator = MainOrchestrator()
await orchestrator.initialize()
await orchestrator.start()
```

**Independent**: ❌ No - Requires all other modules (integration layer)

---

### 5. `singularis-skyrim` 🎮
**Purpose**: Skyrim AGI environment and control

**Contains**:
```
singularis-skyrim/
├── skyrim/
│   ├── skyrim_agi.py
│   ├── game_state.py
│   ├── action_arbiter.py
│   ├── world_model.py
│   └── sensorimotor/
│       ├── vision.py
│       └── motor.py
├── tests/
├── requirements.txt
├── setup.py
└── README.md
```

**Dependencies**:
- OpenCV
- PyAutoGUI
- WebSocket client
- NumPy

**External Module Dependencies**:
- `singularis-core` (consciousness)
- `singularis-perception` (vision)

**API Surface**:
```python
from skyrim import SkyrimAGI

# Initialize
agi = SkyrimAGI(consciousness=consciousness)
await agi.run()
```

**Independent**: ⚠️ Partial - Requires `singularis-core`

---

### 6. `singularis-deployment` 🚀
**Purpose**: Deployment configs, docs, and infrastructure

**Contains**:
```
singularis-deployment/
├── docker/
│   ├── Dockerfile.core
│   ├── Dockerfile.lifeops
│   ├── Dockerfile.integrations
│   └── docker-compose.yml
├── kubernetes/
│   ├── core-deployment.yaml
│   ├── lifeops-deployment.yaml
│   └── ingress.yaml
├── monitoring/
│   ├── prometheus.yml
│   ├── grafana-dashboards/
│   └── alerts.yml
├── docs/
│   ├── SEPHIROT_CLUSTER_ARCHITECTURE.md
│   ├── DEPLOYMENT_CHECKLIST.md
│   └── API_REFERENCE.md
└── README.md
```

**Dependencies**: None (documentation and configs only)

**Independent**: ✅ Yes - Pure infrastructure

---

## Dependency Graph

```
┌─────────────────────────────────────────────┐
│         singularis-integrations             │
│         (Main Orchestrator)                 │
└────────────┬────────────────────────────────┘
             │
    ┌────────┼────────┬────────────┐
    │        │        │            │
    v        v        v            v
┌────────┐ ┌──────┐ ┌──────────┐ ┌────────┐
│ core   │ │lifeops│ │perception│ │skyrim  │
│  🧠    │ │  📊   │ │   👁️     │ │  🎮    │
└────────┘ └───┬───┘ └──────────┘ └───┬────┘
               │                       │
               └───────┬───────────────┘
                       │
                       v
                  ┌────────┐
                  │  core  │
                  │   🧠   │
                  └────────┘
```

**Key**:
- `core`: No dependencies (foundation)
- `perception`: No dependencies (standalone)
- `lifeops`: Depends on `core`
- `skyrim`: Depends on `core`, `perception`
- `integrations`: Depends on all modules

---

## Module Communication

### 1. Direct Import (Same Process)
```python
# When modules are in same deployment
from singularis.consciousness import UnifiedConsciousnessLayer
from lifeops import LifeTimeline
```

### 2. REST API (Microservices)
```python
# When modules are separate services
import requests

response = requests.post(
    'http://core-service:8080/process',
    json={'query': 'hello', 'context': '...'}
)
```

### 3. Message Queue (Async)
```python
# When modules are distributed
import redis

redis_client = redis.Redis(host='message-bus')
redis_client.publish('consciousness.query', json.dumps(data))
```

---

## Repository Setup Scripts

### Create Separate Repos

```bash
#!/bin/bash
# create_modular_repos.sh

# 1. Create singularis-core
mkdir -p ../singularis-core
cp -r singularis/consciousness ../singularis-core/singularis/
cp -r singularis/llm ../singularis-core/singularis/
cp -r singularis/core ../singularis-core/singularis/
cp -r singularis/learning ../singularis-core/singularis/
cp requirements.txt ../singularis-core/
cd ../singularis-core && git init && cd -

# 2. Create singularis-lifeops
mkdir -p ../singularis-lifeops
cp -r integrations/life_timeline.py ../singularis-lifeops/lifeops/
cp -r integrations/pattern_engine.py ../singularis-lifeops/lifeops/
cp -r integrations/intervention_policy.py ../singularis-lifeops/lifeops/
cp -r singularis/life_ops ../singularis-lifeops/lifeops/
cd ../singularis-lifeops && git init && cd -

# 3. Create singularis-perception
mkdir -p ../singularis-perception
cp -r singularis/perception ../singularis-perception/
cd ../singularis-perception && git init && cd -

# 4. Create singularis-integrations
mkdir -p ../singularis-integrations
cp -r integrations/*.py ../singularis-integrations/integrations/
cd ../singularis-integrations && git init && cd -

# 5. Create singularis-skyrim
mkdir -p ../singularis-skyrim
cp -r singularis/skyrim ../singularis-skyrim/
cp run_skyrim_agi.py ../singularis-skyrim/
cd ../singularis-skyrim && git init && cd -

# 6. Create singularis-deployment
mkdir -p ../singularis-deployment
cp -r docs ../singularis-deployment/
cp SEPHIROT_CLUSTER_ARCHITECTURE.md ../singularis-deployment/docs/
cp DEPLOYMENT_CHECKLIST.md ../singularis-deployment/docs/
cd ../singularis-deployment && git init && cd -

echo "✅ All modular repos created!"
```

---

## Setup.py for Each Module

### singularis-core/setup.py
```python
from setuptools import setup, find_packages

setup(
    name="singularis-core",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "openai>=1.0.0",
        "google-generativeai>=0.3.0",
        "loguru>=0.7.0",
        "pydantic>=2.0.0",
        "numpy>=1.24.0",
    ],
    python_requires=">=3.11",
    author="Your Name",
    description="Singularis Core AGI Consciousness",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
```

### singularis-lifeops/setup.py
```python
from setuptools import setup, find_packages

setup(
    name="singularis-lifeops",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "singularis-core>=1.0.0",  # External dependency
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "scikit-learn>=1.3.0",
        "sqlalchemy>=2.0.0",
    ],
    python_requires=">=3.11",
    author="Your Name",
    description="Singularis Life Operations & Timeline",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
```

### singularis-perception/setup.py
```python
from setuptools import setup, find_packages

setup(
    name="singularis-perception",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "opencv-python>=4.8.0",
        "pillow>=10.0.0",
        "google-generativeai>=0.3.0",
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "pygame-ce>=2.4.0",
    ],
    python_requires=">=3.11",
    author="Your Name",
    description="Singularis Perception (Vision & Audio)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
```

---

## Installation Patterns

### Pattern 1: Monolithic (Current)
```bash
# Install everything
git clone https://github.com/user/Singularis.git
cd Singularis
pip install -r requirements.txt
```

### Pattern 2: Modular (Separate Repos)
```bash
# Install only what you need
pip install singularis-core
pip install singularis-lifeops
pip install singularis-perception
```

### Pattern 3: Hybrid (Core + Specific Modules)
```bash
# Install core + specific modules
pip install singularis-core
pip install singularis-skyrim  # For Skyrim AGI only
```

### Pattern 4: Microservices (Docker)
```bash
# Deploy as separate services
docker-compose up core lifeops integrations
```

---

## Migration Strategy

### Phase 1: Prepare (Current)
- [x] Identify module boundaries
- [x] Document dependencies
- [x] Create setup.py for each module
- [ ] Add __init__.py with clear exports

### Phase 2: Restructure (Week 1)
- [ ] Move files to module directories
- [ ] Update imports
- [ ] Create separate requirements.txt per module
- [ ] Test each module independently

### Phase 3: Extract (Week 2)
- [ ] Create separate Git repos
- [ ] Push each module to its repo
- [ ] Set up CI/CD per repo
- [ ] Publish to PyPI (optional)

### Phase 4: Integrate (Week 3)
- [ ] Update main repo to use module imports
- [ ] Test integration
- [ ] Update documentation
- [ ] Deploy to Sephirot cluster

---

## Module Versioning

### Semantic Versioning
```
MAJOR.MINOR.PATCH

singularis-core: 1.0.0
singularis-lifeops: 1.0.0
singularis-perception: 1.0.0
```

### Compatibility Matrix
```
core 1.0.x ← lifeops 1.0.x ✅
core 1.0.x ← lifeops 1.1.x ✅
core 1.0.x ← lifeops 2.0.x ❌

core 1.1.x ← lifeops 1.0.x ✅
core 2.0.x ← lifeops 1.0.x ❌
```

---

## Testing Strategy

### Per-Module Tests
```bash
# Test core independently
cd singularis-core
pytest tests/

# Test lifeops independently
cd singularis-lifeops
pytest tests/

# Test perception independently
cd singularis-perception
pytest tests/
```

### Integration Tests
```bash
# Test module interactions
cd singularis-integrations
pytest tests/test_integration.py
```

---

## Deployment Patterns

### Pattern 1: Monolithic Deployment
```yaml
# docker-compose.yml
services:
  singularis:
    image: singularis-all:latest
    ports:
      - "8080:8080"
```

### Pattern 2: Microservices Deployment
```yaml
# docker-compose.yml
services:
  core:
    image: singularis-core:latest
    ports:
      - "8081:8080"
  
  lifeops:
    image: singularis-lifeops:latest
    ports:
      - "8082:8080"
    depends_on:
      - core
  
  integrations:
    image: singularis-integrations:latest
    ports:
      - "8080:8080"
    depends_on:
      - core
      - lifeops
```

### Pattern 3: Kubernetes Deployment
```yaml
# kubernetes/core-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: singularis-core
spec:
  replicas: 2
  selector:
    matchLabels:
      app: singularis-core
  template:
    metadata:
      labels:
        app: singularis-core
    spec:
      containers:
      - name: core
        image: singularis-core:1.0.0
        ports:
        - containerPort: 8080
```

---

## Benefits of Modular Architecture

### Development
- ✅ Independent development cycles
- ✅ Smaller, focused codebases
- ✅ Easier to test
- ✅ Clear ownership

### Deployment
- ✅ Deploy only what you need
- ✅ Scale modules independently
- ✅ Reduce resource usage
- ✅ Faster deployments

### Maintenance
- ✅ Easier to debug
- ✅ Isolated failures
- ✅ Independent updates
- ✅ Clear dependencies

### Reusability
- ✅ Use modules in other projects
- ✅ Share modules with community
- ✅ Mix and match as needed
- ✅ Build on top of modules

---

## Example Use Cases

### Use Case 1: Life Ops Only
```bash
# Just want life tracking, no Skyrim
pip install singularis-core
pip install singularis-lifeops
pip install singularis-integrations

# Run
python -m integrations.main_orchestrator
```

### Use Case 2: Skyrim AGI Only
```bash
# Just want Skyrim AGI
pip install singularis-core
pip install singularis-perception
pip install singularis-skyrim

# Run
python -m skyrim.run_agi
```

### Use Case 3: Custom Integration
```bash
# Build your own integration
pip install singularis-core

# Your code
from singularis.consciousness import UnifiedConsciousnessLayer

consciousness = UnifiedConsciousnessLayer()
# ... your custom logic
```

---

## Next Steps

### Immediate (This Week)
1. [ ] Create setup.py for each module
2. [ ] Add __init__.py with clear exports
3. [ ] Document module APIs
4. [ ] Test module independence

### Short-term (Next 2 Weeks)
1. [ ] Restructure file layout
2. [ ] Update all imports
3. [ ] Create separate repos
4. [ ] Set up CI/CD

### Long-term (Next Month)
1. [ ] Publish to PyPI
2. [ ] Create module documentation sites
3. [ ] Build example projects
4. [ ] Community adoption

---

**Status**: 📋 **READY TO MODULARIZE**

**Next**: Run `create_modular_repos.sh` to extract modules into separate repos

**Goal**: Independent, reusable, composable AGI modules 🧩✨
