# Sephirot Cluster Architecture 🌳

**Distributed AGI Infrastructure - No NUC Design**

---

## Overview

The **Sephirot** cluster is a distributed AGI system inspired by the Kabbalistic Tree of Life, where each node represents a different aspect of consciousness and cognition. This architecture eliminates the NUC and redistributes its duties across the existing hardware.

---

## Node Layout

### 🧠 Node A — Primary Cognitive & Control Plane
**Hardware**: AMD Tower (dual AMD Radeon 7900 XT)  
**Role**: Core brain + orchestration + APIs  
**Metaphor**: "Cortex + Brainstem"

**Runs**:
- ✅ Singularis core consciousness
  - BeingState/LifeState management
  - Neuron networks
  - ActionArbiter
  - Temporal binding
  - Unified Consciousness Layer
- ✅ API Gateway (REST/gRPC)
  - `/lifeops/*` endpoints
  - `/choice` endpoint
  - `/timeline` endpoints
  - `/query` endpoint (Phase 5)
- ✅ Message bus
  - Redis/NGINX/ZeroMQ/Kafka-lite
  - Event streaming
  - Task queue
- ✅ Orchestration services
  - Job scheduler
  - Experiment routing
  - Service mesh
- ✅ Light monitoring agents
  - Node exporters
  - Log collectors

**Network**: Static IP on local network  
**Storage**: Fast NVMe for hot data, state snapshots  
**GPU Usage**: Dual 7900 XT for inference, embeddings, vision processing

---

### 🧬 Node B — Memory & Observability
**Hardware**: Desktop (AMD Radeon 6900 XT)  
**Role**: Long-term memory + metrics stack  
**Metaphor**: "Hippocampus + Data Warehouse"

**Runs**:
- ✅ Vector databases
  - ChromaDB for embeddings
  - Episodic memory storage
  - Semantic memory consolidation
- ✅ SQL/NoSQL databases
  - Life Timeline (SQLite/PostgreSQL)
  - Event logs
  - LifeOps history
  - Pattern database
- ✅ Monitoring stack
  - Prometheus (metrics collection)
  - Grafana (dashboards)
  - Loki/ELK (log aggregation)
- ✅ Analytics services
  - Offline pattern analysis
  - Nearline data processing
  - Historical correlation analysis

**Network**: Static IP on local network  
**Storage**: Large HDD/SSD array for long-term storage  
**GPU Usage**: 6900 XT for batch embeddings, analytics

---

### 🕹️ Node C — Real-Time Environment / Embodiment
**Hardware**: Gaming Laptop (NVIDIA RTX)  
**Role**: Simulation + real-time action loop  
**Metaphor**: "Body + Sensorimotor Surface"

**Runs**:
- ✅ Skyrim / game environments
- ✅ Real-time control loop
  - Sends state snapshots → Node A
  - Receives actions/decisions ← Node A
  - Executes actions in environment
- ✅ Telemetry agent
  - FPS monitoring
  - Latency tracking
  - Success/fail statistics → Node B
- ✅ Screen capture
- ✅ Input injection

**Network**: WiFi/Ethernet to Node A  
**Storage**: Game files, state cache  
**GPU Usage**: RTX for game rendering + vision inference

---

### 📱 Node D — Camera Monitor & Home Surveillance
**Hardware**: Lenovo Tab (Android)  
**Role**: Camera feed aggregation + screen capture source  
**Metaphor**: "Eyes of the Home"

**Runs**:
- ✅ Roku Smart Home app
  - Displays all camera feeds in grid
  - Live view of all rooms
  - Motion detection alerts
- ✅ ADB server (wireless)
  - Allows screen capture via `adb shell screencap`
  - Enables remote control
- ✅ Always-on display mode
  - Mounted on wall/stand
  - Continuous monitoring

**Setup**:
1. Install Roku Smart Home app
2. Configure all cameras in app
3. Enable Developer Mode:
   ```
   Settings → About → Tap "Build number" 7 times
   Settings → Developer options → Enable USB debugging
   Settings → Developer options → Enable Wireless debugging
   ```
4. Connect via ADB:
   ```bash
   adb connect <LENOVO_TAB_IP>:5555
   ```
5. Keep screen always on (via app or settings)

**Network**: WiFi to Node A  
**Power**: Always plugged in  
**Position**: Wall-mounted or stand in central location

---

### 💻 Node E — Dev & Operator Console
**Hardware**: MacBook Pro  
**Role**: Human interface  
**Metaphor**: "Operator's Terminal"

**Used For**:
- ✅ Development
  - VS Code / Windsurf
  - SSH to all nodes
  - Git operations
  - Docker/K8s tooling
- ✅ Monitoring
  - Grafana dashboards (Node B)
  - Prometheus queries
  - Log inspection
- ✅ Operations
  - Manually trigger experiments
  - Restart services
  - Deploy updates
  - Debug issues

**Network**: WiFi/Ethernet to all nodes  
**Storage**: Local dev environment, Git repos  
**No Infrastructure**: Pure client device

---

### 📱 Edge Devices

#### Phone
**Role**: Mobile interface + sensor hub

**Capabilities**:
- ✅ Calls Node A APIs:
  - `POST /lifeops/event` (life events)
  - `POST /choice` (decision requests)
  - `GET /timeline` (query history)
  - `POST /query` (natural language queries)
- ✅ Fitbit integration
  - Health metrics
  - Sleep data
  - Activity tracking
- ✅ Messenger bot interface
  - Natural language interaction
  - Life queries
  - Pattern insights

#### Meta Glasses
**Role**: Wearable vision + audio

**Capabilities**:
- ✅ Stream audio/video → Phone → Node A
- ✅ Real-time vision analysis (Gemini 2.5 Flash)
- ✅ Voice interaction
- ✅ Contextual awareness

---

## Network Topology

```
                    ┌─────────────────────────────────┐
                    │   🧠 Node A: AMD Tower          │
                    │   (Cortex + Brainstem)          │
                    │   - Singularis Core             │
                    │   - API Gateway                 │
                    │   - Message Bus                 │
                    │   - Orchestration               │
                    └──────────┬──────────────────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                v              v              v
    ┌───────────────────┐  ┌──────────────┐  ┌──────────────────┐
    │ 🧬 Node B         │  │ 🕹️ Node C    │  │ 📱 Node D        │
    │ (Hippocampus)     │  │ (Body)       │  │ (Eyes)           │
    │ - Vector DB       │  │ - Skyrim     │  │ - Lenovo Tab     │
    │ - SQL/NoSQL       │  │ - Control    │  │ - Roku App       │
    │ - Prometheus      │  │ - Telemetry  │  │ - ADB Server     │
    │ - Grafana         │  │              │  │ - Camera Feeds   │
    └───────────────────┘  └──────────────┘  └──────────────────┘
                │                                      │
                │                                      │ (screencap)
                │                                      v
                │                              [Node A processes]
                │
                v (dashboards)
    ┌───────────────────┐
    │ 💻 Node E         │
    │ (Operator)        │
    │ - MacBook Pro     │
    │ - Dev Tools       │
    │ - Monitoring UI   │
    └───────────────────┘

    ┌─────────────┐         ┌──────────────┐
    │ 📱 Phone    │────────>│ 🧠 Node A    │
    │ - Fitbit    │  HTTP   │              │
    │ - Messenger │         │              │
    └─────────────┘         └──────────────┘
         ^
         │ (stream)
    ┌─────────────┐
    │ 👓 Glasses  │
    │ - Audio     │
    │ - Video     │
    └─────────────┘
```

---

## Data Flow Examples

### 1. Camera Event Detection (AGI Vision)

```
Lenovo Tab (Roku App showing cameras)
    ↓ (ADB screencap)
Node A (RokuScreenCaptureGateway)
    ↓ (extract camera regions)
Node A (VideoInterpreter - Gemini 2.5 Flash)
    ↓ (AGI analysis: "Person walking in kitchen")
Node A (Extract events: person_detected, motion_detected)
    ↓ (store events)
Node B (Life Timeline database)
    ↓ (metrics)
Node B (Prometheus/Grafana)
```

### 2. Life Query (Natural Language)

```
Phone (Messenger): "How did I sleep last week?"
    ↓ (HTTPS)
Node A (MessengerBotAdapter)
    ↓ (detect life query keywords)
Node A (LifeQueryHandler)
    ↓ (query timeline)
Node B (Life Timeline database)
    ↓ (return 7 sleep events)
Node A (LifeQueryHandler)
    ↓ (build context + AGI analysis)
Node A (UnifiedConsciousnessLayer)
    ↓ (generate insights)
Node A (Response: "You averaged 7.2 hours...")
    ↓ (HTTPS)
Phone (Messenger): [Display response]
```

### 3. Skyrim AGI Action Loop

```
Node C (Skyrim running)
    ↓ (screenshot + game state)
Node A (SkyrimAGI)
    ↓ (vision analysis)
Node A (GPT-5 + MoE experts)
    ↓ (decide action: "attack enemy")
Node C (execute action)
    ↓ (telemetry: success/fail, FPS, latency)
Node B (Prometheus metrics)
    ↓ (dashboard)
Node E (Grafana: view performance)
```

### 4. Pattern Detection & Intervention

```
Node B (Pattern Engine - scheduled job)
    ↓ (query last 24h events)
Node B (Life Timeline)
    ↓ (detect: "sedentary for 3 hours")
Node A (AGI Pattern Arbiter)
    ↓ (analyze context: time of day, mood, routine)
Node A (AGI Intervention Decider)
    ↓ (decide: "gentle reminder via voice")
Node A (Voice System)
    ↓ (TTS: "You've been sitting for a while...")
Phone (play audio notification)
```

---

## Hardware Requirements

### Node A (AMD Tower)
- **CPU**: High-core count (Ryzen 9 or Threadripper)
- **GPU**: Dual AMD Radeon 7900 XT (48GB VRAM total)
- **RAM**: 64GB+ DDR5
- **Storage**: 2TB+ NVMe SSD
- **Network**: Gigabit Ethernet (static IP)
- **OS**: Ubuntu 22.04 LTS or Windows 11

### Node B (Desktop)
- **CPU**: Mid-range (Ryzen 7)
- **GPU**: AMD Radeon 6900 XT (16GB VRAM)
- **RAM**: 32GB+ DDR4
- **Storage**: 4TB+ HDD/SSD (RAID for redundancy)
- **Network**: Gigabit Ethernet (static IP)
- **OS**: Ubuntu 22.04 LTS

### Node C (Gaming Laptop)
- **CPU**: Intel i7/i9 or Ryzen 7/9
- **GPU**: NVIDIA RTX 3060+ (8GB+ VRAM)
- **RAM**: 16GB+ DDR4
- **Storage**: 1TB+ NVMe SSD
- **Network**: WiFi 6 or Gigabit Ethernet
- **OS**: Windows 11

### Node D (Lenovo Tab)
- **Model**: Lenovo Tab P11/P12 or similar
- **OS**: Android 11+
- **RAM**: 4GB+
- **Storage**: 64GB+
- **Display**: 10-12" (always-on capable)
- **Network**: WiFi 5/6
- **Power**: Always plugged in

### Node E (MacBook Pro)
- **Model**: M1/M2/M3 MacBook Pro
- **RAM**: 16GB+
- **Storage**: 512GB+
- **Network**: WiFi 6

---

## Software Stack

### Node A (Cognitive Core)
```yaml
Core Services:
  - Singularis AGI (Python 3.11+)
  - FastAPI (REST API)
  - Redis (message bus)
  - NGINX (reverse proxy)
  - Docker/Docker Compose

Dependencies:
  - PyTorch 2.0+
  - Transformers (Hugging Face)
  - OpenAI SDK (GPT-5)
  - Google Generative AI (Gemini)
  - Loguru (logging)
```

### Node B (Memory & Metrics)
```yaml
Databases:
  - ChromaDB (vector store)
  - PostgreSQL (structured data)
  - SQLite (Life Timeline)

Monitoring:
  - Prometheus (metrics)
  - Grafana (dashboards)
  - Loki (logs)
  - Node Exporter (system metrics)

Analytics:
  - Pandas/NumPy
  - Scikit-learn
  - Jupyter (notebooks)
```

### Node C (Environment)
```yaml
Environment:
  - Skyrim Special Edition
  - Mod Organizer 2
  - SKSE64

Integration:
  - Python 3.11+
  - OpenCV (screen capture)
  - PyAutoGUI (input injection)
  - WebSocket client
```

### Node D (Camera Monitor)
```yaml
Apps:
  - Roku Smart Home (camera feeds)
  - ADB Wireless (remote access)
  - Tasker (automation - optional)

Configuration:
  - Developer Mode enabled
  - Wireless debugging enabled
  - Always-on display
```

### Node E (Dev Console)
```yaml
Tools:
  - VS Code / Windsurf
  - Docker Desktop
  - Git
  - SSH client
  - Web browser (Grafana access)
```

---

## Network Configuration

### Static IPs (Recommended)

```bash
Node A (AMD Tower):     192.168.1.10
Node B (Desktop):       192.168.1.11
Node C (Laptop):        192.168.1.12 (or DHCP)
Node D (Lenovo Tab):    192.168.1.13
Node E (MacBook):       DHCP (client only)
Phone:                  DHCP
```

### Port Assignments

```yaml
Node A:
  - 8080: Main API (FastAPI)
  - 6379: Redis
  - 80/443: NGINX (reverse proxy)
  - 9090: Prometheus (if local)

Node B:
  - 5432: PostgreSQL
  - 9090: Prometheus
  - 3000: Grafana
  - 3100: Loki

Node C:
  - 8081: Telemetry API (optional)

Node D:
  - 5555: ADB wireless
```

### Firewall Rules

```bash
# Node A (allow from all nodes)
ufw allow from 192.168.1.0/24 to any port 8080
ufw allow from 192.168.1.0/24 to any port 6379

# Node B (allow from Node A and Node E)
ufw allow from 192.168.1.10 to any port 5432
ufw allow from 192.168.1.0/24 to any port 3000

# Node D (allow from Node A only)
# Configure via Android firewall app if needed
```

---

## Deployment Steps

### 1. Node A Setup (AMD Tower)

```bash
# Install OS (Ubuntu 22.04 LTS)
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Python 3.11+
sudo apt install python3.11 python3.11-venv python3-pip

# Clone Singularis
git clone https://github.com/yourusername/Singularis.git
cd Singularis

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
nano .env  # Configure API keys, IPs

# Install AMD GPU drivers
# (Follow AMD ROCm installation guide)

# Start services
docker-compose up -d redis nginx

# Run Singularis
cd integrations
python main_orchestrator.py
```

### 2. Node B Setup (Desktop)

```bash
# Install OS (Ubuntu 22.04 LTS)
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Deploy monitoring stack
cd monitoring
docker-compose up -d

# Configure Prometheus targets
nano prometheus.yml
# Add Node A, Node C exporters

# Configure Grafana dashboards
# Access http://192.168.1.11:3000
# Import dashboards from grafana/

# Set up databases
docker run -d -p 5432:5432 \
  -e POSTGRES_PASSWORD=yourpassword \
  -v pgdata:/var/lib/postgresql/data \
  postgres:15

# Install ChromaDB
pip install chromadb
python -m chromadb.server --host 0.0.0.0
```

### 3. Node C Setup (Gaming Laptop)

```bash
# Install Skyrim + mods
# (Follow SKYRIM_INTEGRATION_ISSUES.md)

# Install Python 3.11+
# Download from python.org

# Clone Singularis
git clone https://github.com/yourusername/Singularis.git
cd Singularis

# Install dependencies
pip install -r requirements.txt

# Configure Node A connection
nano .env
# Set NODE_A_URL=http://192.168.1.10:8080

# Run Skyrim AGI
python run_skyrim_agi.py
```

### 4. Node D Setup (Lenovo Tab)

```bash
# On Lenovo Tab:
1. Install Roku Smart Home app from Play Store
2. Configure all cameras in app
3. Enable Developer Mode:
   Settings → About → Tap "Build number" 7 times
4. Enable USB debugging:
   Settings → Developer options → USB debugging ON
5. Enable Wireless debugging:
   Settings → Developer options → Wireless debugging ON
6. Get IP address:
   Settings → About → Status → IP address
7. Keep screen always on:
   Settings → Display → Screen timeout → Never
   OR install "Keep Screen On" app

# On Node A (AMD Tower):
# Connect via ADB
adb connect 192.168.1.13:5555

# Test screen capture
adb shell screencap -p /sdcard/test.png
adb pull /sdcard/test.png

# Configure in .env
echo "RASPBERRY_PI_IP=192.168.1.13" >> .env
echo "ROKU_ADB_PORT=5555" >> .env
echo "ENABLE_ROKU_CAMERAS=true" >> .env
```

### 5. Node E Setup (MacBook Pro)

```bash
# Install development tools
brew install git docker
brew install --cask visual-studio-code

# Clone Singularis
git clone https://github.com/yourusername/Singularis.git

# Configure SSH access to all nodes
ssh-keygen -t ed25519
ssh-copy-id user@192.168.1.10  # Node A
ssh-copy-id user@192.168.1.11  # Node B

# Bookmark Grafana
open http://192.168.1.11:3000

# Install monitoring tools
brew install prometheus grafana
```

---

## Environment Variables

### Node A (.env)
```bash
# API Keys
GEMINI_API_KEY=your_gemini_key
OPENAI_API_KEY=your_openai_key

# Node Configuration
NODE_A_IP=192.168.1.10
NODE_B_IP=192.168.1.11

# Camera Configuration
ENABLE_ROKU_CAMERAS=true
RASPBERRY_PI_IP=192.168.1.13
ROKU_ADB_PORT=5555
ROKU_FPS=2
ROKU_CAMERA_MAPPING={"cam1":"living_room","cam2":"kitchen","cam3":"bedroom"}

# AGI Vision
ENABLE_AGI_VISION=true

# Messenger Bot
MESSENGER_PAGE_TOKEN=your_page_token
MESSENGER_VERIFY_TOKEN=your_verify_token

# Fitbit
FITBIT_CLIENT_ID=your_client_id
FITBIT_CLIENT_SECRET=your_client_secret
```

---

## Monitoring & Observability

### Grafana Dashboards (Node B)

Access: `http://192.168.1.11:3000`

**Dashboards**:
1. **System Overview**
   - CPU/RAM/GPU usage per node
   - Network traffic
   - Disk I/O

2. **AGI Performance**
   - API latency (p50, p95, p99)
   - Request rate
   - Error rate
   - GPU utilization

3. **Life Timeline**
   - Events per hour
   - Event types breakdown
   - Data sources (Fitbit, Camera, Messenger)

4. **Camera Vision**
   - AGI analyses per minute
   - Detection types (person, motion, fall)
   - Confidence scores
   - API costs

5. **Skyrim AGI**
   - Actions per minute
   - Success rate
   - FPS
   - Latency (state → action)

### Prometheus Metrics

**Node A Exports**:
```
singularis_api_requests_total
singularis_api_latency_seconds
singularis_gpu_utilization_percent
singularis_consciousness_coherence_score
singularis_timeline_events_total
```

**Node C Exports**:
```
skyrim_fps
skyrim_action_success_rate
skyrim_latency_ms
```

---

## Maintenance

### Daily
- ✅ Check Grafana dashboards for anomalies
- ✅ Review error logs on Node A
- ✅ Verify all services running

### Weekly
- ✅ Backup Life Timeline database (Node B)
- ✅ Review API costs (Gemini, OpenAI)
- ✅ Update dependencies
- ✅ Clean up old logs

### Monthly
- ✅ Full system backup
- ✅ Performance optimization
- ✅ Security updates
- ✅ Capacity planning

---

## Troubleshooting

### Node A Not Responding
```bash
# SSH to Node A
ssh user@192.168.1.10

# Check services
docker ps
systemctl status singularis

# Check logs
tail -f logs/main_orchestrator.log

# Restart if needed
systemctl restart singularis
```

### Node D (Lenovo Tab) ADB Connection Lost
```bash
# Reconnect
adb connect 192.168.1.13:5555

# If fails, on Lenovo Tab:
# Settings → Developer options → Wireless debugging → OFF → ON

# Get new port if changed
adb devices
```

### Camera Feeds Not Processing
```bash
# Check ADB connection
adb devices

# Test screen capture
adb shell screencap -p /sdcard/test.png

# Check logs
tail -f logs/roku_screencap_gateway.log

# Verify Roku app is running on Lenovo Tab
```

### High API Costs
```bash
# Check Gemini usage
grep "GEMINI" logs/*.log | wc -l

# Reduce AGI vision frame rate
# In .env: ROKU_FPS=1 (instead of 2)

# Disable AGI vision temporarily
# In .env: ENABLE_AGI_VISION=false
```

---

## Security Considerations

### Network Security
- ✅ All nodes on private network (192.168.1.x)
- ✅ Firewall rules limiting access
- ✅ No external ports exposed (use VPN for remote access)

### API Keys
- ✅ Store in `.env` files (not in Git)
- ✅ Use environment variables
- ✅ Rotate keys periodically

### Data Privacy
- ✅ Life Timeline data stays local (Node B)
- ✅ Camera feeds processed locally
- ✅ Only AGI analysis sent to cloud (Gemini)

### Access Control
- ✅ SSH key-based authentication
- ✅ Grafana password-protected
- ✅ API authentication tokens

---

## Cost Estimates

### Hardware (One-Time)
- Node A (AMD Tower): $2,500-3,500
- Node B (Desktop): $1,500-2,000
- Node C (Gaming Laptop): $1,500-2,500
- Node D (Lenovo Tab): $200-400
- **Total**: ~$5,700-8,400

### Cloud Services (Monthly)
- Gemini API (AGI vision + queries): $50-150
- OpenAI API (GPT-5): $100-300
- **Total**: ~$150-450/month

### Electricity (Monthly)
- Node A (24/7): ~$30
- Node B (24/7): ~$20
- Node C (8h/day): ~$10
- Node D (24/7): ~$5
- **Total**: ~$65/month

**Grand Total**: ~$215-515/month operating cost

---

## Performance Targets

### Latency
- API response (Node A): < 100ms (p95)
- Life query (with AGI): < 3s
- Camera event detection: < 2s
- Skyrim action loop: < 500ms

### Throughput
- API requests: 100+ req/s
- Camera frames: 2 FPS (AGI), 10 FPS (CV)
- Life events: 1000+ events/day
- Queries: 10+ queries/hour

### Reliability
- Node A uptime: 99.9%
- Node B uptime: 99.5%
- Data loss: 0%
- API error rate: < 1%

---

## Future Enhancements

### Phase 6: Advanced Features
- ✅ Multi-user support
- ✅ Predictive insights
- ✅ Voice queries
- ✅ Visualization dashboards
- ✅ Mobile app

### Phase 7: Scaling
- ✅ Kubernetes orchestration
- ✅ Load balancing
- ✅ Horizontal scaling
- ✅ Edge computing

### Phase 8: Intelligence
- ✅ Self-optimization
- ✅ Autonomous learning
- ✅ Goal emergence
- ✅ Creative problem-solving

---

**Sephirot Cluster Status**: 📋 **READY TO DEPLOY**

All software complete. Hardware setup is the final step! 🚀

**Next**: Follow deployment steps for each node and start the AGI! 🌳✨
