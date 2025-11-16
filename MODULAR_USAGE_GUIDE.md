# Modular Usage Guide 🧩

**How to use Singularis as independent modules**

---

## Quick Start

### Option 1: Install Everything (Monolithic)
```bash
# Clone main repo
git clone https://github.com/yourusername/Singularis.git
cd Singularis
pip install -r requirements.txt

# Run
python integrations/main_orchestrator.py
```

### Option 2: Install Specific Modules (Modular)
```bash
# Install only what you need
pip install singularis-core
pip install singularis-lifeops

# Use in your code
from singularis.consciousness import UnifiedConsciousnessLayer
from lifeops import LifeTimeline
```

---

## Module Catalog

### 1. singularis-core 🧠
**What it does**: Core AGI consciousness and reasoning

**Install**:
```bash
pip install singularis-core
```

**Use**:
```python
from singularis.consciousness import UnifiedConsciousnessLayer
from singularis.core import BeingState

# Initialize
consciousness = UnifiedConsciousnessLayer()

# Process query
result = await consciousness.process_unified(
    query="What should I do today?",
    context="User is feeling tired",
    being_state=BeingState()
)

print(result.response)
```

**When to use**:
- Building AGI applications
- Need advanced reasoning
- Want consciousness-level processing

---

### 2. singularis-lifeops 📊
**What it does**: Life Timeline, patterns, interventions, queries

**Install**:
```bash
pip install singularis-core  # Required dependency
pip install singularis-lifeops
```

**Use**:
```python
from lifeops import LifeTimeline, PatternEngine
from lifeops.life_ops import LifeQueryHandler
from singularis.consciousness import UnifiedConsciousnessLayer

# Initialize
timeline = LifeTimeline("data/timeline.db")
consciousness = UnifiedConsciousnessLayer()
query_handler = LifeQueryHandler(consciousness, timeline)

# Add events
from lifeops import create_camera_event
event = create_camera_event(
    user_id="user123",
    room="living_room",
    event_type="person_detected"
)
timeline.add_event(event)

# Query
result = await query_handler.handle_query(
    "user123",
    "How did I sleep last week?"
)
print(result.response)
```

**When to use**:
- Life tracking applications
- Health monitoring
- Pattern detection
- Natural language queries about life data

---

### 3. singularis-perception 👁️
**What it does**: Vision, audio, and multimodal processing

**Install**:
```bash
pip install singularis-perception
```

**Use**:
```python
from perception import StreamingVideoInterpreter
from PIL import Image

# Initialize
interpreter = StreamingVideoInterpreter(
    mode="comprehensive",
    frame_rate=0.5
)

# Analyze frame
frame = Image.open("camera_feed.jpg")
analysis = await interpreter.analyze_frame(frame)

print(analysis['interpretation'])
```

**When to use**:
- Computer vision applications
- Real-time video analysis
- Audio processing
- Multimodal AI

---

### 4. singularis-integrations 🔌
**What it does**: External service adapters (Messenger, Fitbit, cameras)

**Install**:
```bash
pip install singularis-core
pip install singularis-lifeops
pip install singularis-perception
pip install singularis-integrations
```

**Use**:
```python
from integrations import MainOrchestrator

# Initialize
orchestrator = MainOrchestrator()
await orchestrator.initialize()

# Start all integrations
await orchestrator.start()

# Access via API
# GET http://localhost:8080/health
# POST http://localhost:8080/query
```

**When to use**:
- Full system deployment
- Need all integrations
- Building complete life ops system

---

### 5. singularis-skyrim 🎮
**What it does**: Skyrim AGI environment and control

**Install**:
```bash
pip install singularis-core
pip install singularis-perception
pip install singularis-skyrim
```

**Use**:
```python
from skyrim import SkyrimAGI
from singularis.consciousness import UnifiedConsciousnessLayer

# Initialize
consciousness = UnifiedConsciousnessLayer()
agi = SkyrimAGI(consciousness=consciousness)

# Run
await agi.run()
```

**When to use**:
- Skyrim AI research
- Game AI development
- Embodied AGI experiments

---

## Common Use Cases

### Use Case 1: Life Tracking Only

**Goal**: Track life events and query them

**Modules needed**:
- `singularis-core` (for AGI queries)
- `singularis-lifeops` (for timeline)

**Setup**:
```bash
pip install singularis-core singularis-lifeops
```

**Code**:
```python
from lifeops import LifeTimeline
from lifeops.life_ops import LifeQueryHandler
from singularis.consciousness import UnifiedConsciousnessLayer

# Initialize
timeline = LifeTimeline("my_life.db")
consciousness = UnifiedConsciousnessLayer()
query_handler = LifeQueryHandler(consciousness, timeline)

# Add events (from Fitbit, cameras, etc.)
# ... add events ...

# Query
result = await query_handler.handle_query(
    "me",
    "What patterns do you see in my routine?"
)
print(result.response)
```

---

### Use Case 2: Vision Analysis Only

**Goal**: Analyze video feeds with AGI

**Modules needed**:
- `singularis-perception` (standalone)

**Setup**:
```bash
pip install singularis-perception
```

**Code**:
```python
from perception import StreamingVideoInterpreter
import cv2

# Initialize
interpreter = StreamingVideoInterpreter(mode="comprehensive")

# Capture frame
cap = cv2.VideoCapture(0)
ret, frame = cap.read()

# Convert to PIL
from PIL import Image
frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
pil_frame = Image.fromarray(frame_rgb)

# Analyze
analysis = await interpreter.analyze_frame(pil_frame)
print(analysis['interpretation'])
```

---

### Use Case 3: Custom Chatbot

**Goal**: Build a chatbot with AGI consciousness

**Modules needed**:
- `singularis-core` (for consciousness)

**Setup**:
```bash
pip install singularis-core
```

**Code**:
```python
from singularis.consciousness import UnifiedConsciousnessLayer
from singularis.core import BeingState

# Initialize
consciousness = UnifiedConsciousnessLayer()
being_state = BeingState()

# Chat loop
while True:
    user_input = input("You: ")
    
    result = await consciousness.process_unified(
        query=user_input,
        context="Friendly conversation",
        being_state=being_state
    )
    
    print(f"Bot: {result.response}")
    
    # Update being state
    being_state = result.being_state
```

---

### Use Case 4: Full Life Ops System

**Goal**: Complete life tracking with all features

**Modules needed**:
- All modules

**Setup**:
```bash
pip install singularis-core
pip install singularis-lifeops
pip install singularis-perception
pip install singularis-integrations
```

**Code**:
```python
from integrations import MainOrchestrator

# Initialize
orchestrator = MainOrchestrator()
await orchestrator.initialize()

# Start all services
await orchestrator.start()

# Access via:
# - Messenger bot
# - REST API (http://localhost:8080)
# - Direct Python calls
```

---

## Development Workflow

### Working on Single Module

```bash
# Clone module repo
git clone https://github.com/yourusername/singularis-core.git
cd singularis-core

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install in editable mode
pip install -e .

# Install dev dependencies
pip install -e ".[dev]"

# Make changes
# ... edit code ...

# Run tests
pytest tests/

# Format code
black singularis/

# Lint
flake8 singularis/

# Commit
git add .
git commit -m "feat: add new feature"
git push
```

---

### Working on Multiple Modules

```bash
# Clone all modules
git clone https://github.com/yourusername/singularis-core.git
git clone https://github.com/yourusername/singularis-lifeops.git

# Install core in editable mode
cd singularis-core
pip install -e .
cd ..

# Install lifeops in editable mode (will use local core)
cd singularis-lifeops
pip install -e .
cd ..

# Now changes in core are immediately visible in lifeops
```

---

### Testing Integration

```bash
# Install all modules in editable mode
pip install -e ../singularis-core
pip install -e ../singularis-lifeops
pip install -e ../singularis-perception
pip install -e ../singularis-integrations

# Run integration tests
cd singularis-integrations
pytest tests/test_integration.py
```

---

## Publishing to PyPI

### 1. Prepare Module

```bash
cd singularis-core

# Update version in setup.py
# version="1.0.1"

# Build distribution
python -m build

# This creates:
# dist/singularis-core-1.0.1.tar.gz
# dist/singularis_core-1.0.1-py3-none-any.whl
```

### 2. Test on TestPyPI

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Test install
pip install --index-url https://test.pypi.org/simple/ singularis-core
```

### 3. Publish to PyPI

```bash
# Upload to PyPI
python -m twine upload dist/*

# Now anyone can install
pip install singularis-core
```

---

## Docker Deployment

### Single Module

```dockerfile
# Dockerfile.core
FROM python:3.11-slim

WORKDIR /app

# Install module
RUN pip install singularis-core

# Copy your app
COPY app.py .

# Run
CMD ["python", "app.py"]
```

### Multiple Modules

```dockerfile
# Dockerfile.integrations
FROM python:3.11-slim

WORKDIR /app

# Install all modules
RUN pip install singularis-core \
                singularis-lifeops \
                singularis-perception \
                singularis-integrations

# Copy config
COPY .env .

# Run orchestrator
CMD ["python", "-m", "integrations.main_orchestrator"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  core:
    image: singularis-core:latest
    ports:
      - "8081:8080"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
  
  lifeops:
    image: singularis-lifeops:latest
    ports:
      - "8082:8080"
    depends_on:
      - core
    environment:
      - CORE_URL=http://core:8080
  
  integrations:
    image: singularis-integrations:latest
    ports:
      - "8080:8080"
    depends_on:
      - core
      - lifeops
    environment:
      - CORE_URL=http://core:8080
      - LIFEOPS_URL=http://lifeops:8080
```

---

## Version Compatibility

### Semantic Versioning

```
MAJOR.MINOR.PATCH

1.0.0 → 1.0.1 (patch: bug fixes)
1.0.1 → 1.1.0 (minor: new features, backward compatible)
1.1.0 → 2.0.0 (major: breaking changes)
```

### Compatibility Matrix

| Core | LifeOps | Perception | Integrations |
|------|---------|------------|--------------|
| 1.0.x | 1.0.x | 1.0.x | 1.0.x | ✅ Compatible
| 1.1.x | 1.0.x | 1.0.x | 1.0.x | ✅ Compatible
| 2.0.x | 1.0.x | 1.0.x | 1.0.x | ❌ Incompatible
| 1.0.x | 1.1.x | 1.0.x | 1.0.x | ✅ Compatible
| 1.0.x | 2.0.x | 1.0.x | 1.0.x | ⚠️ Check docs

### Pinning Versions

```python
# setup.py - Pin exact versions
install_requires=[
    "singularis-core==1.0.0",  # Exact version
]

# setup.py - Allow patch updates
install_requires=[
    "singularis-core>=1.0.0,<1.1.0",  # 1.0.x only
]

# setup.py - Allow minor updates
install_requires=[
    "singularis-core>=1.0.0,<2.0.0",  # 1.x.x only
]
```

---

## Troubleshooting

### Module Not Found

```bash
# Check installation
pip list | grep singularis

# Reinstall
pip uninstall singularis-core
pip install singularis-core

# Check import path
python -c "import singularis; print(singularis.__file__)"
```

### Version Conflicts

```bash
# Check versions
pip show singularis-core
pip show singularis-lifeops

# Update to compatible versions
pip install singularis-core==1.0.0 singularis-lifeops==1.0.0
```

### Import Errors

```python
# Wrong import
from singularis.lifeops import LifeTimeline  # ❌

# Correct import
from lifeops import LifeTimeline  # ✅
```

---

## Best Practices

### 1. Use Virtual Environments
```bash
python -m venv venv
source venv/bin/activate
```

### 2. Pin Dependencies
```python
# requirements.txt
singularis-core==1.0.0
singularis-lifeops==1.0.0
```

### 3. Test Before Deploying
```bash
pytest tests/
```

### 4. Use Semantic Versioning
```
1.0.0 → 1.0.1 (bug fix)
1.0.1 → 1.1.0 (new feature)
1.1.0 → 2.0.0 (breaking change)
```

### 5. Document Dependencies
```markdown
# README.md
## Dependencies
- singularis-core >= 1.0.0
- singularis-lifeops >= 1.0.0
```

---

## Next Steps

1. **Extract modules**: Run `scripts/create_modular_repos.ps1`
2. **Test independently**: Test each module in isolation
3. **Publish**: Push to GitHub, publish to PyPI
4. **Document**: Write READMEs for each module
5. **Deploy**: Use in production

---

**Status**: 📋 **READY TO USE**

**Choose your path**:
- 🏗️ **Monolithic**: Clone main repo, install everything
- 🧩 **Modular**: Install only what you need
- 🐳 **Docker**: Deploy as microservices
- 📦 **PyPI**: Publish and share with community

Good luck! 🚀✨
