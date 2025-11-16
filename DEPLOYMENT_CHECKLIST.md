# Sephirot Cluster Deployment Checklist ✅

**Quick reference for deploying the complete AGI system**

---

## Pre-Deployment

### Hardware Inventory
- [ ] AMD Tower (dual 7900 XT) - Node A
- [ ] Desktop (6900 XT) - Node B  
- [ ] Gaming Laptop (RTX) - Node C
- [ ] Lenovo Tab (Android) - Node D
- [ ] MacBook Pro - Node E
- [ ] Phone (with Fitbit)
- [ ] Meta Glasses (optional)
- [ ] Network switch/router
- [ ] Ethernet cables (Cat6)
- [ ] Power strips/UPS

### Software Prerequisites
- [ ] Ubuntu 22.04 ISO (for Node A, B)
- [ ] Windows 11 (for Node C)
- [ ] Roku Smart Home app APK
- [ ] API keys ready:
  - [ ] Gemini API key
  - [ ] OpenAI API key
  - [ ] Messenger page token
  - [ ] Fitbit credentials

---

## Node A: AMD Tower (Cognitive Core)

### OS Installation
- [ ] Install Ubuntu 22.04 LTS
- [ ] Set static IP: 192.168.1.10
- [ ] Update system: `sudo apt update && sudo apt upgrade -y`
- [ ] Install SSH: `sudo apt install openssh-server`
- [ ] Configure hostname: `sudo hostnamectl set-hostname node-a`

### GPU Drivers
- [ ] Install AMD ROCm drivers
- [ ] Verify GPU detection: `rocm-smi`
- [ ] Test both 7900 XT cards visible

### Docker Setup
- [ ] Install Docker: `curl -fsSL https://get.docker.com | sh`
- [ ] Add user to docker group: `sudo usermod -aG docker $USER`
- [ ] Install Docker Compose: `sudo apt install docker-compose`
- [ ] Test: `docker run hello-world`

### Python Environment
- [ ] Install Python 3.11: `sudo apt install python3.11 python3.11-venv`
- [ ] Install pip: `sudo apt install python3-pip`
- [ ] Create venv: `python3.11 -m venv venv`
- [ ] Activate: `source venv/bin/activate`

### Singularis Installation
- [ ] Clone repo: `git clone <repo_url> ~/Singularis`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Copy .env: `cp .env.example .env`
- [ ] Configure .env with API keys
- [ ] Set Node B IP in .env: `NODE_B_IP=192.168.1.11`

### Services
- [ ] Start Redis: `docker run -d -p 6379:6379 redis:7`
- [ ] Start NGINX: `docker run -d -p 80:80 nginx`
- [ ] Test API: `curl http://localhost:8080/health`

### Verification
- [ ] Run: `cd integrations && python main_orchestrator.py`
- [ ] Check logs: `tail -f logs/main_orchestrator.log`
- [ ] Test API: `curl http://192.168.1.10:8080/health`
- [ ] Verify GPU usage: `rocm-smi`

---

## Node B: Desktop (Memory & Metrics)

### OS Installation
- [ ] Install Ubuntu 22.04 LTS
- [ ] Set static IP: 192.168.1.11
- [ ] Update system: `sudo apt update && sudo apt upgrade -y`
- [ ] Install SSH: `sudo apt install openssh-server`
- [ ] Configure hostname: `sudo hostnamectl set-hostname node-b`

### GPU Drivers
- [ ] Install AMD ROCm drivers
- [ ] Verify GPU: `rocm-smi`

### Docker Setup
- [ ] Install Docker: `curl -fsSL https://get.docker.com | sh`
- [ ] Install Docker Compose: `sudo apt install docker-compose`

### Databases
- [ ] Start PostgreSQL:
  ```bash
  docker run -d -p 5432:5432 \
    -e POSTGRES_PASSWORD=yourpassword \
    -v pgdata:/var/lib/postgresql/data \
    --name postgres postgres:15
  ```
- [ ] Start ChromaDB:
  ```bash
  docker run -d -p 8000:8000 \
    -v chromadb:/chroma/chroma \
    --name chromadb chromadb/chroma
  ```
- [ ] Test connections

### Monitoring Stack
- [ ] Create monitoring directory: `mkdir -p ~/monitoring`
- [ ] Create docker-compose.yml:
  ```yaml
  version: '3'
  services:
    prometheus:
      image: prom/prometheus:latest
      ports:
        - "9090:9090"
      volumes:
        - ./prometheus.yml:/etc/prometheus/prometheus.yml
        - prometheus-data:/prometheus
    
    grafana:
      image: grafana/grafana:latest
      ports:
        - "3000:3000"
      volumes:
        - grafana-data:/var/lib/grafana
    
    loki:
      image: grafana/loki:latest
      ports:
        - "3100:3100"
  
  volumes:
    prometheus-data:
    grafana-data:
  ```
- [ ] Start: `docker-compose up -d`

### Prometheus Configuration
- [ ] Create prometheus.yml:
  ```yaml
  global:
    scrape_interval: 15s
  
  scrape_configs:
    - job_name: 'node-a'
      static_configs:
        - targets: ['192.168.1.10:9090']
    
    - job_name: 'node-c'
      static_configs:
        - targets: ['192.168.1.12:9091']
  ```
- [ ] Reload Prometheus

### Grafana Setup
- [ ] Access: http://192.168.1.11:3000
- [ ] Login: admin/admin (change password)
- [ ] Add Prometheus data source
- [ ] Import dashboards from repo

### Verification
- [ ] Prometheus: http://192.168.1.11:9090
- [ ] Grafana: http://192.168.1.11:3000
- [ ] PostgreSQL: `psql -h 192.168.1.11 -U postgres`
- [ ] ChromaDB: `curl http://192.168.1.11:8000/api/v1/heartbeat`

---

## Node C: Gaming Laptop (Environment)

### OS Setup
- [ ] Install Windows 11
- [ ] Set IP: 192.168.1.12 (or DHCP)
- [ ] Update Windows
- [ ] Install GPU drivers (NVIDIA)

### Skyrim Installation
- [ ] Install Steam
- [ ] Install Skyrim Special Edition
- [ ] Install SKSE64
- [ ] Install Mod Organizer 2
- [ ] Install required mods (see SKYRIM_INTEGRATION_ISSUES.md)

### Python Environment
- [ ] Download Python 3.11 from python.org
- [ ] Install with "Add to PATH" checked
- [ ] Verify: `python --version`
- [ ] Install pip: `python -m ensurepip`

### Singularis Installation
- [ ] Clone repo: `git clone <repo_url> C:\Singularis`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Copy .env: `copy .env.example .env`
- [ ] Configure .env:
  ```
  NODE_A_URL=http://192.168.1.10:8080
  ```

### Verification
- [ ] Run: `python run_skyrim_agi.py`
- [ ] Launch Skyrim
- [ ] Verify AGI control
- [ ] Check telemetry: http://192.168.1.11:3000

---

## Node D: Lenovo Tab (Camera Monitor)

### Initial Setup
- [ ] Power on Lenovo Tab
- [ ] Connect to WiFi
- [ ] Update Android OS
- [ ] Set static IP: 192.168.1.13 (in WiFi settings)

### Roku Smart Home App
- [ ] Install from Play Store
- [ ] Sign in to Roku account
- [ ] Add all cameras:
  - [ ] Living room camera
  - [ ] Kitchen camera
  - [ ] Bedroom camera
  - [ ] (Add more as needed)
- [ ] Verify all feeds visible
- [ ] Set to grid view (all cameras at once)

### Developer Mode
- [ ] Go to Settings → About
- [ ] Tap "Build number" 7 times
- [ ] Developer options now visible
- [ ] Settings → Developer options:
  - [ ] Enable "USB debugging"
  - [ ] Enable "Wireless debugging"
  - [ ] Note the IP and port

### Display Settings
- [ ] Settings → Display:
  - [ ] Screen timeout → Never (or use "Stay Alive" app)
  - [ ] Brightness → Auto or 70%
- [ ] Install "Keep Screen On" app (optional)
- [ ] Configure to keep Roku app always visible

### ADB Connection (from Node A)
- [ ] On Node A: `adb connect 192.168.1.13:5555`
- [ ] Verify: `adb devices` (should show device)
- [ ] Test screencap: `adb shell screencap -p /sdcard/test.png`
- [ ] Pull test: `adb pull /sdcard/test.png`
- [ ] Verify image shows camera feeds

### Mounting
- [ ] Mount tablet on wall or stand
- [ ] Position for easy viewing
- [ ] Ensure power cable reaches
- [ ] Keep plugged in 24/7

### Verification
- [ ] Roku app showing all cameras
- [ ] Screen stays on
- [ ] ADB connection stable
- [ ] Test screencap from Node A

---

## Node E: MacBook Pro (Dev Console)

### Development Tools
- [ ] Install Homebrew: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
- [ ] Install Git: `brew install git`
- [ ] Install VS Code: `brew install --cask visual-studio-code`
- [ ] Install Docker Desktop: `brew install --cask docker`

### Repository Setup
- [ ] Clone repo: `git clone <repo_url> ~/Singularis`
- [ ] Open in VS Code: `code ~/Singularis`

### SSH Configuration
- [ ] Generate SSH key: `ssh-keygen -t ed25519`
- [ ] Copy to Node A: `ssh-copy-id user@192.168.1.10`
- [ ] Copy to Node B: `ssh-copy-id user@192.168.1.11`
- [ ] Test: `ssh user@192.168.1.10`

### Monitoring Access
- [ ] Bookmark Grafana: http://192.168.1.11:3000
- [ ] Bookmark Prometheus: http://192.168.1.11:9090
- [ ] Test access from browser

### Verification
- [ ] SSH to all nodes works
- [ ] Grafana accessible
- [ ] Git operations work
- [ ] VS Code connected to repo

---

## Edge Devices

### Phone Setup
- [ ] Install Messenger app
- [ ] Install Fitbit app
- [ ] Link Fitbit account
- [ ] Configure Fitbit sync
- [ ] Test Messenger bot: Send message to page
- [ ] Verify bot responds

### Meta Glasses (Optional)
- [ ] Pair with phone
- [ ] Install Meta View app
- [ ] Configure streaming
- [ ] Test audio/video capture

---

## Network Configuration

### Router Setup
- [ ] Reserve static IPs:
  - [ ] 192.168.1.10 → Node A MAC address
  - [ ] 192.168.1.11 → Node B MAC address
  - [ ] 192.168.1.13 → Node D MAC address
- [ ] Port forwarding (if remote access needed):
  - [ ] 8080 → Node A (API)
  - [ ] 3000 → Node B (Grafana)

### Firewall Rules
- [ ] Node A: Allow 8080, 6379 from local network
- [ ] Node B: Allow 3000, 9090, 5432 from local network
- [ ] Node D: Allow 5555 from Node A only

### DNS (Optional)
- [ ] Add local DNS entries:
  - [ ] node-a.local → 192.168.1.10
  - [ ] node-b.local → 192.168.1.11
  - [ ] grafana.local → 192.168.1.11:3000

---

## Integration Testing

### API Tests
- [ ] From Node E: `curl http://192.168.1.10:8080/health`
- [ ] Test message: `curl -X POST http://192.168.1.10:8080/message -d '{"user_id":"test","content":"hello"}'`
- [ ] Test query: `curl -X POST http://192.168.1.10:8080/query -d '{"user_id":"test","query":"How did I sleep?"}'`

### Camera Tests
- [ ] Verify ADB connection: `adb devices`
- [ ] Test screencap: `adb shell screencap -p /sdcard/test.png`
- [ ] Start camera gateway on Node A
- [ ] Verify events in timeline: `curl http://192.168.1.10:8080/timeline`

### Messenger Bot Tests
- [ ] Send message to bot
- [ ] Verify response
- [ ] Test life query: "How did I sleep last week?"
- [ ] Verify AGI-powered response

### Skyrim AGI Tests
- [ ] Launch Skyrim on Node C
- [ ] Start AGI: `python run_skyrim_agi.py`
- [ ] Verify AGI controls character
- [ ] Check Grafana for metrics

### Monitoring Tests
- [ ] Open Grafana: http://192.168.1.11:3000
- [ ] Verify all dashboards load
- [ ] Check metrics from Node A, C
- [ ] Verify no errors in Prometheus

---

## Environment Variables

### Node A (.env)
```bash
# API Keys
GEMINI_API_KEY=your_gemini_key_here
OPENAI_API_KEY=your_openai_key_here

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
MESSENGER_PAGE_TOKEN=your_messenger_token_here
MESSENGER_VERIFY_TOKEN=your_verify_token_here

# Fitbit
FITBIT_CLIENT_ID=your_fitbit_client_id
FITBIT_CLIENT_SECRET=your_fitbit_client_secret
```

---

## Post-Deployment

### Monitoring Setup
- [ ] Configure Grafana alerts
- [ ] Set up email notifications
- [ ] Create custom dashboards
- [ ] Configure log retention

### Backup Configuration
- [ ] Set up automated backups for Node B databases
- [ ] Configure backup schedule (daily)
- [ ] Test restore procedure
- [ ] Document backup locations

### Documentation
- [ ] Document custom configurations
- [ ] Create runbook for common issues
- [ ] Document API endpoints
- [ ] Create user guide

### Security Hardening
- [ ] Change default passwords
- [ ] Configure SSH key-only auth
- [ ] Enable firewall on all nodes
- [ ] Review API key security
- [ ] Set up VPN for remote access (optional)

---

## Validation Checklist

### System Health
- [ ] All nodes responding to ping
- [ ] All services running (docker ps)
- [ ] No errors in logs
- [ ] GPU utilization normal
- [ ] Disk space adequate (>20% free)

### Functionality
- [ ] API endpoints responding
- [ ] Camera feeds processing
- [ ] Messenger bot working
- [ ] Life queries returning results
- [ ] Skyrim AGI controlling game
- [ ] Metrics collecting in Prometheus

### Performance
- [ ] API latency < 100ms (p95)
- [ ] Camera processing < 2s per frame
- [ ] Life queries < 3s
- [ ] Skyrim action loop < 500ms
- [ ] No memory leaks

### Data Flow
- [ ] Events flowing to timeline
- [ ] Metrics flowing to Prometheus
- [ ] Logs flowing to Loki
- [ ] Embeddings storing in ChromaDB

---

## Troubleshooting

### Node A Not Starting
```bash
# Check logs
tail -f ~/Singularis/logs/main_orchestrator.log

# Check Python
python --version

# Check dependencies
pip list | grep -i singularis

# Restart
cd ~/Singularis/integrations
python main_orchestrator.py
```

### Node D ADB Connection Issues
```bash
# Reconnect
adb disconnect
adb connect 192.168.1.13:5555

# If fails, on tablet:
# Toggle wireless debugging OFF then ON
# Note new port if changed

# Verify
adb devices
```

### Grafana Not Loading
```bash
# Check Docker
docker ps | grep grafana

# Check logs
docker logs grafana

# Restart
docker restart grafana
```

### High API Costs
```bash
# Check usage
grep "GEMINI" ~/Singularis/logs/*.log | wc -l

# Reduce frame rate
# In .env: ROKU_FPS=1

# Disable AGI vision temporarily
# In .env: ENABLE_AGI_VISION=false
```

---

## Success Criteria

### Deployment Complete When:
- [x] All 5 nodes operational
- [x] All services running
- [x] API responding
- [x] Camera feeds processing
- [x] Messenger bot working
- [x] Monitoring dashboards live
- [x] No critical errors
- [x] Performance targets met

### Ready for Production When:
- [x] 24-hour stability test passed
- [x] All integrations tested
- [x] Backups configured
- [x] Documentation complete
- [x] Team trained
- [x] Runbook created

---

**Deployment Status**: 📋 **READY TO BEGIN**

**Estimated Time**: 8-12 hours (spread over 2-3 days)

**Next Step**: Start with Node A (AMD Tower) setup

Good luck! 🚀✨
