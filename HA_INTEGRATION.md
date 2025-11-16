# Home Assistant Integration Guide

**Integrating Singularis Life Ops with Home Assistant**

This guide shows how to connect Home Assistant (your smart home hub) with Singularis Life Ops (your personal AGI) to create a closed-loop intelligent system.

---

## Overview

**Goal**: Home Assistant feeds real-world sensor data into Life Timeline, and Life Ops sends intelligent suggestions/actions back to Home Assistant.

**Architecture**:
```
Home Assistant Sensors → Life Timeline (SQLite)
                              ↓
                    Pattern Engine + AGI
                              ↓
                    Suggestions/Actions → Home Assistant → Notifications/Devices
```

**What You Get**:
- All smart home events (presence, motion, doors, climate, etc.) logged in Life Timeline
- AGI-powered pattern detection (anomalies, habits, correlations)
- Proactive suggestions delivered to phone/AR glasses via Home Assistant notifications
- Optional: autonomous home control based on Life Ops decisions

---

## Prerequisites

- **Home Assistant** running (any version 2023+)
- **Singularis Life Ops** running (`python integrations/main_orchestrator.py`)
- Both on same network (or accessible via internet with proper security)
- API keys configured (OpenAI/Gemini for AGI features)

---

## Part 1: Home Assistant → Life Ops (Context In)

### Option A: REST API (Simplest to Start)

#### 1. Add HA Event Endpoint to Life Ops

Edit `integrations/main_orchestrator.py`, add this endpoint after the existing routes:

```python
@app.post("/ha/event")
async def receive_ha_event(
    user_id: str,
    source: str,
    event_type: str,
    features: Optional[Dict] = None,
    timestamp: Optional[str] = None
):
    """
    Receive event from Home Assistant.
    
    POST /ha/event
    {
        "user_id": "main_user",
        "source": "ha",
        "event_type": "arrive_home",
        "features": {"zone": "home", "device": "phone"},
        "timestamp": "2025-11-16T12:00:00"
    }
    """
    if not orchestrator:
        raise HTTPException(status_code=500, detail="Orchestrator not initialized")
    
    from life_timeline import LifeEvent, EventSource, EventType
    from datetime import datetime
    import uuid
    
    # Map HA event types to Life Timeline types
    type_mapping = {
        'arrive_home': EventType.ARRIVE_HOME,
        'leave_home': EventType.LEAVE_HOME,
        'room_enter': EventType.ROOM_ENTER,
        'room_exit': EventType.ROOM_EXIT,
        'door_open': EventType.DOOR_OPEN,
        'motion': EventType.ROOM_ENTER,  # Treat motion as room activity
        'sleep_start': EventType.SLEEP,
        'exercise_start': EventType.EXERCISE,
        'work_start': EventType.WORK_SESSION,
        'break_start': EventType.BREAK,
        # Add more as needed
    }
    
    # Get EventType
    try:
        if event_type in type_mapping:
            evt_type = type_mapping[event_type]
        else:
            evt_type = EventType.OTHER
    except:
        evt_type = EventType.OTHER
    
    # Create event
    event = LifeEvent(
        id=f"ha_{uuid.uuid4().hex[:12]}",
        user_id=user_id,
        timestamp=datetime.fromisoformat(timestamp) if timestamp else datetime.now(),
        source=EventSource.MANUAL if source == "ha" else EventSource(source),
        type=evt_type,
        features=features or {},
        confidence=1.0,
        importance=0.5
    )
    
    # Add to timeline
    success = orchestrator.timeline.add_event(event)
    
    if success:
        logger.info(f"[HA-BRIDGE] Event added: {event_type} for {user_id}")
        return {"status": "ok", "event_id": event.id}
    else:
        raise HTTPException(status_code=500, detail="Failed to add event")
```

#### 2. Configure Home Assistant REST Command

Add to your `configuration.yaml`:

```yaml
rest_command:
  lifeops_event:
    url: "http://<LIFEOPS_IP>:8080/ha/event"
    method: POST
    content_type: "application/json"
    payload: >
      {
        "user_id": "main_user",
        "source": "ha",
        "event_type": "{{ event_type }}",
        "features": {{ features | tojson }},
        "timestamp": "{{ now().isoformat() }}"
      }
```

Replace `<LIFEOPS_IP>` with your Life Ops server IP (e.g., `192.168.1.100` or `localhost`).

#### 3. Create Automations to Send Events

**Example: Track Home Arrival/Departure**

```yaml
automation:
  - id: lifeops_arrive_home
    alias: "Life Ops: Arrive Home"
    trigger:
      - platform: state
        entity_id: person.your_name
        to: "home"
    action:
      - service: rest_command.lifeops_event
        data:
          event_type: "arrive_home"
          features:
            zone: "home"
            device: "{{ trigger.to_state.attributes.source }}"
  
  - id: lifeops_leave_home
    alias: "Life Ops: Leave Home"
    trigger:
      - platform: state
        entity_id: person.your_name
        from: "home"
    action:
      - service: rest_command.lifeops_event
        data:
          event_type: "leave_home"
          features:
            zone: "{{ trigger.to_state.state }}"
```

**Example: Track Room Activity**

```yaml
automation:
  - id: lifeops_room_motion
    alias: "Life Ops: Room Motion"
    trigger:
      - platform: state
        entity_id:
          - binary_sensor.living_room_motion
          - binary_sensor.bedroom_motion
          - binary_sensor.office_motion
        to: "on"
    action:
      - service: rest_command.lifeops_event
        data:
          event_type: "room_enter"
          features:
            room: "{{ trigger.to_state.name | replace(' Motion', '') }}"
            sensor: "{{ trigger.entity_id }}"
```

**Example: Track Door Events**

```yaml
automation:
  - id: lifeops_door_open
    alias: "Life Ops: Door Opened"
    trigger:
      - platform: state
        entity_id:
          - binary_sensor.front_door
          - binary_sensor.back_door
        to: "on"
    action:
      - service: rest_command.lifeops_event
        data:
          event_type: "door_open"
          features:
            door: "{{ trigger.to_state.name }}"
            timestamp: "{{ now().isoformat() }}"
```

### Option B: MQTT (Better for High-Frequency Updates)

#### 1. Set Up MQTT Broker

If not already running, install Mosquitto add-on in Home Assistant or run externally.

#### 2. Configure Home Assistant MQTT

In `configuration.yaml`:

```yaml
mqtt:
  broker: localhost  # or your MQTT broker IP
  port: 1883
  username: !secret mqtt_username
  password: !secret mqtt_password
```

#### 3. Publish HA Events to MQTT

```yaml
automation:
  - id: lifeops_mqtt_presence
    alias: "Life Ops MQTT: Presence"
    trigger:
      - platform: state
        entity_id: person.your_name
    action:
      - service: mqtt.publish
        data:
          topic: "lifeops/event/presence"
          payload: >
            {
              "user_id": "main_user",
              "event_type": "{{ 'arrive_home' if trigger.to_state.state == 'home' else 'leave_home' }}",
              "features": {
                "zone": "{{ trigger.to_state.state }}",
                "source": "{{ trigger.to_state.attributes.source }}"
              },
              "timestamp": "{{ now().isoformat() }}"
            }
```

#### 4. Subscribe in Life Ops

Create `integrations/ha_mqtt_bridge.py`:

```python
"""
MQTT Bridge for Home Assistant → Life Timeline
"""

import asyncio
import json
from datetime import datetime
from typing import Optional
import paho.mqtt.client as mqtt
from loguru import logger

from life_timeline import LifeTimeline, LifeEvent, EventSource, EventType
import uuid


class HAMQTTBridge:
    """Bridge Home Assistant MQTT messages to Life Timeline."""
    
    def __init__(
        self,
        timeline: LifeTimeline,
        broker: str = "localhost",
        port: int = 1883,
        username: Optional[str] = None,
        password: Optional[str] = None,
        user_id: str = "main_user"
    ):
        self.timeline = timeline
        self.user_id = user_id
        
        # MQTT client
        self.client = mqtt.Client()
        if username and password:
            self.client.username_pw_set(username, password)
        
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        
        self.broker = broker
        self.port = port
        
        logger.info(f"[HA-MQTT] Bridge initialized (broker: {broker}:{port})")
    
    def _on_connect(self, client, userdata, flags, rc):
        """Callback when connected to MQTT broker."""
        if rc == 0:
            logger.info("[HA-MQTT] Connected to broker")
            # Subscribe to all lifeops topics
            client.subscribe("lifeops/#")
            logger.info("[HA-MQTT] Subscribed to lifeops/#")
        else:
            logger.error(f"[HA-MQTT] Connection failed: {rc}")
    
    def _on_message(self, client, userdata, msg):
        """Callback when message received."""
        try:
            payload = json.loads(msg.payload.decode())
            
            # Extract event data
            event_type = payload.get('event_type', 'other')
            features = payload.get('features', {})
            timestamp_str = payload.get('timestamp')
            user_id = payload.get('user_id', self.user_id)
            
            # Parse timestamp
            if timestamp_str:
                timestamp = datetime.fromisoformat(timestamp_str)
            else:
                timestamp = datetime.now()
            
            # Map to EventType
            type_mapping = {
                'arrive_home': EventType.ARRIVE_HOME,
                'leave_home': EventType.LEAVE_HOME,
                'room_enter': EventType.ROOM_ENTER,
                'room_exit': EventType.ROOM_EXIT,
                'door_open': EventType.DOOR_OPEN,
                'motion': EventType.ROOM_ENTER,
                'sleep': EventType.SLEEP,
                'exercise': EventType.EXERCISE,
                'work': EventType.WORK_SESSION,
                'break': EventType.BREAK,
            }
            
            evt_type = type_mapping.get(event_type, EventType.OTHER)
            
            # Create event
            event = LifeEvent(
                id=f"ha_{uuid.uuid4().hex[:12]}",
                user_id=user_id,
                timestamp=timestamp,
                source=EventSource.MANUAL,  # Or create EventSource.HOME_ASSISTANT
                type=evt_type,
                features=features,
                confidence=1.0,
                importance=0.5
            )
            
            # Add to timeline
            success = self.timeline.add_event(event)
            
            if success:
                logger.info(f"[HA-MQTT] Event added: {event_type} (topic: {msg.topic})")
            else:
                logger.error(f"[HA-MQTT] Failed to add event: {event_type}")
        
        except Exception as e:
            logger.error(f"[HA-MQTT] Error processing message: {e}")
    
    def start(self):
        """Start MQTT client (blocking)."""
        logger.info(f"[HA-MQTT] Connecting to {self.broker}:{self.port}...")
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_forever()
    
    def start_async(self):
        """Start MQTT client in background thread."""
        import threading
        thread = threading.Thread(target=self.start, daemon=True)
        thread.start()
        logger.info("[HA-MQTT] Bridge started in background")
```

Add to `main_orchestrator.py` initialization:

```python
# After timeline initialization
if os.getenv('ENABLE_HA_MQTT', 'false').lower() == 'true':
    from ha_mqtt_bridge import HAMQTTBridge
    
    logger.info("[ORCHESTRATOR] Initializing HA MQTT bridge...")
    self.ha_mqtt_bridge = HAMQTTBridge(
        timeline=self.timeline,
        broker=os.getenv('MQTT_BROKER', 'localhost'),
        port=int(os.getenv('MQTT_PORT', '1883')),
        username=os.getenv('MQTT_USERNAME'),
        password=os.getenv('MQTT_PASSWORD'),
        user_id="main_user"
    )
    self.ha_mqtt_bridge.start_async()
    logger.info("[ORCHESTRATOR] ✅ HA MQTT bridge started")
```

---

## Part 2: Life Ops → Home Assistant (Suggestions Out)

### Option A: Home Assistant Webhook (Simplest)

#### 1. Create Webhook Automation in HA

```yaml
automation:
  - id: lifeops_suggestion_handler
    alias: "Life Ops: Handle Suggestion"
    trigger:
      - platform: webhook
        webhook_id: lifeops-suggestions-webhook
    action:
      - choose:
          # High priority suggestions - immediate notification
          - conditions:
              - condition: template
                value_template: "{{ trigger.json.priority in ['HIGH', 'CRITICAL'] }}"
            sequence:
              - service: notify.mobile_app_your_phone
                data:
                  title: "⚠️ Life Ops Alert"
                  message: "{{ trigger.json.suggestion }}"
                  data:
                    actions:
                      - action: "ACCEPT_{{ trigger.json.binding_id }}"
                        title: "Accept"
                      - action: "DECLINE_{{ trigger.json.binding_id }}"
                        title: "Decline"
          
          # Normal suggestions - gentle notification
          - conditions:
              - condition: template
                value_template: "{{ trigger.json.priority == 'MEDIUM' }}"
            sequence:
              - service: notify.mobile_app_your_phone
                data:
                  title: "💡 Life Ops Suggestion"
                  message: "{{ trigger.json.suggestion }}"
                  data:
                    actions:
                      - action: "ACCEPT_{{ trigger.json.binding_id }}"
                        title: "Yes"
                      - action: "DECLINE_{{ trigger.json.binding_id }}"
                        title: "No"
        
        default:
          - service: logbook.log
            data:
              name: "Life Ops"
              message: "{{ trigger.json.suggestion }}"
```

#### 2. Send Suggestions from Life Ops

Add to `integrations/main_orchestrator.py` or create `integrations/suggestion_sender.py`:

```python
import aiohttp
from loguru import logger

async def send_suggestion_to_ha(
    suggestion: str,
    priority: str = "MEDIUM",
    binding_id: str = None,
    suggestion_type: str = "general",
    ha_url: str = "http://homeassistant.local:8123"
):
    """
    Send suggestion to Home Assistant webhook.
    
    Args:
        suggestion: Text of the suggestion
        priority: LOW, MEDIUM, HIGH, CRITICAL
        binding_id: Unique ID for tracking
        suggestion_type: Type of suggestion (focus, break, comfort, etc.)
        ha_url: Home Assistant URL
    """
    webhook_url = f"{ha_url}/api/webhook/lifeops-suggestions-webhook"
    
    payload = {
        "suggestion": suggestion,
        "priority": priority,
        "binding_id": binding_id or f"{time.time():.6f}",
        "type": suggestion_type,
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook_url, json=payload) as resp:
                if resp.status == 200:
                    logger.info(f"[HA-BRIDGE] Suggestion sent: {suggestion[:50]}...")
                    return True
                else:
                    logger.error(f"[HA-BRIDGE] Failed to send suggestion: {resp.status}")
                    return False
    except Exception as e:
        logger.error(f"[HA-BRIDGE] Error sending suggestion: {e}")
        return False
```

#### 3. Integrate with Pattern Engine

Modify `integrations/pattern_engine.py` to send suggestions:

```python
# At the end of analyze_all() or detect_fall(), etc.
async def analyze_all_with_ha_notifications(self, user_id: str, ha_url: str) -> Dict[str, Any]:
    """Run analysis and send critical alerts to Home Assistant."""
    results = self.analyze_all(user_id)
    
    # Check for critical anomalies
    for anomaly in results.get('anomalies', []):
        if anomaly['alert_level'] in ['CRITICAL', 'HIGH']:
            await send_suggestion_to_ha(
                suggestion=anomaly['message'],
                priority=anomaly['alert_level'],
                binding_id=anomaly['id'],
                suggestion_type='safety_alert',
                ha_url=ha_url
            )
    
    return results
```

### Option B: MQTT Suggestions

#### 1. Publish Suggestions to MQTT

```python
def publish_suggestion_mqtt(
    client: mqtt.Client,
    suggestion: str,
    priority: str = "MEDIUM",
    binding_id: str = None
):
    """Publish suggestion to MQTT."""
    payload = {
        "suggestion": suggestion,
        "priority": priority,
        "binding_id": binding_id or f"{time.time():.6f}",
        "timestamp": datetime.now().isoformat()
    }
    
    client.publish(
        "lifeops/suggestion",
        json.dumps(payload),
        qos=1,
        retain=False
    )
```

#### 2. Subscribe in Home Assistant

```yaml
mqtt:
  sensor:
    - name: "Life Ops Suggestion"
      state_topic: "lifeops/suggestion"
      value_template: "{{ value_json.suggestion }}"
      json_attributes_topic: "lifeops/suggestion"

automation:
  - id: lifeops_mqtt_suggestion
    alias: "Life Ops: MQTT Suggestion"
    trigger:
      - platform: mqtt
        topic: "lifeops/suggestion"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "💡 Life Ops"
          message: "{{ trigger.payload_json.suggestion }}"
```

---

## Part 3: Closing the Loop (User Response)

### Handle User Acceptance/Rejection

#### 1. Capture Response in Home Assistant

```yaml
automation:
  - id: lifeops_response_accept
    alias: "Life Ops: User Accepted"
    trigger:
      - platform: event
        event_type: mobile_app_notification_action
        event_data:
          action: "ACCEPT_*"
    action:
      - service: rest_command.lifeops_response
        data:
          binding_id: "{{ trigger.event.data.action | replace('ACCEPT_', '') }}"
          accepted: true
  
  - id: lifeops_response_decline
    alias: "Life Ops: User Declined"
    trigger:
      - platform: event
        event_type: mobile_app_notification_action
        event_data:
          action: "DECLINE_*"
    action:
      - service: rest_command.lifeops_response
        data:
          binding_id: "{{ trigger.event.data.action | replace('DECLINE_', '') }}"
          accepted: false
```

Add REST command:

```yaml
rest_command:
  lifeops_response:
    url: "http://<LIFEOPS_IP>:8080/ha/response"
    method: POST
    content_type: "application/json"
    payload: >
      {
        "binding_id": "{{ binding_id }}",
        "accepted": {{ accepted }},
        "timestamp": "{{ now().isoformat() }}"
      }
```

#### 2. Handle Response in Life Ops

Add endpoint to `main_orchestrator.py`:

```python
@app.post("/ha/response")
async def receive_ha_response(
    binding_id: str,
    accepted: bool,
    timestamp: Optional[str] = None
):
    """
    Receive user response to suggestion from Home Assistant.
    
    POST /ha/response
    {
        "binding_id": "2025-11-16T12:00:00_focus_block",
        "accepted": true,
        "timestamp": "2025-11-16T12:01:00"
    }
    """
    logger.info(
        f"[HA-BRIDGE] User {'accepted' if accepted else 'declined'} "
        f"suggestion {binding_id}"
    )
    
    # TODO: Update suggestion tracking, trigger actions if accepted
    # For now, just log it
    
    return {
        "status": "ok",
        "binding_id": binding_id,
        "action": "accepted" if accepted else "declined"
    }
```

---

## Part 4: AR Glasses Integration (Meta Ray-Ban)

### How It Works

Meta Ray-Ban Display glasses mirror your phone notifications. Since Home Assistant sends suggestions as mobile notifications, they automatically appear in your AR view.

### Setup

1. **Pair glasses to phone** (via Meta View app)
2. **Enable notifications** for Home Assistant Companion App
3. **Configure notification priority** so Life Ops suggestions appear in glasses

### Interaction

- **View**: Suggestions appear as floating text in your right eye
- **Respond**: Use Neural Band gestures or voice to tap notification actions
- **Result**: Response sent back to Home Assistant → Life Ops

No custom AR app needed - it just works via OS notifications!

---

## Example Use Cases

### 1. Safety Monitoring

**Scenario**: Detect falls or no movement

```yaml
# HA sends motion sensor data to Life Ops
# Life Ops pattern engine detects no movement for 6 hours
# Life Ops sends CRITICAL alert to HA
# HA notifies emergency contact + user's glasses
```

### 2. Focus Sessions

**Scenario**: Suggest deep work blocks

```yaml
# HA tracks: you're home, in office, morning, calendar shows "focus time"
# Life Ops suggests: "Start 25-min focus on Project X?"
# User accepts via glasses
# HA triggers: lights dim, phone DND, timer starts
# After 25 min: HA asks for feedback, sends to Life Ops
```

### 3. Habit Tracking

**Scenario**: Exercise reminders

```yaml
# Life Ops detects: no exercise events for 3 days
# Life Ops suggests: "Go for a 10-min walk?"
# User accepts
# HA tracks: person leaves home, motion detected outside
# HA confirms: "Walk completed!" → Life Ops logs success
```

### 4. Comfort Optimization

**Scenario**: Environmental adjustments

```yaml
# HA sensors: room temp 28°C, you've been in room 2 hours
# Life Ops suggests: "It's warm, turn on AC?"
# User accepts via glasses
# HA executes: climate.turn_on
# Life Ops learns: user prefers AC when temp > 27°C
```

---

## Configuration Reference

### Environment Variables

Add to `.env`:

```bash
# Home Assistant Integration
ENABLE_HA_MQTT=true
MQTT_BROKER=192.168.1.100
MQTT_PORT=1883
MQTT_USERNAME=lifeops
MQTT_PASSWORD=your_mqtt_password

# Home Assistant URL for webhooks
HA_URL=http://homeassistant.local:8123
HA_WEBHOOK_ID=lifeops-suggestions-webhook
```

### Home Assistant Secrets

Add to `secrets.yaml`:

```yaml
lifeops_url: "http://192.168.1.100:8080"
mqtt_username: lifeops
mqtt_password: your_mqtt_password
```

---

## Testing

### 1. Test Event Flow (HA → Life Ops)

```bash
# Trigger a test automation in HA or call REST command manually
curl -X POST http://localhost:8080/ha/event \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "main_user",
    "source": "ha",
    "event_type": "arrive_home",
    "features": {"zone": "home"},
    "timestamp": "2025-11-16T12:00:00"
  }'

# Check Life Timeline
curl http://localhost:8080/stats
```

### 2. Test Suggestion Flow (Life Ops → HA)

```python
# In Python console or test script
import asyncio
from suggestion_sender import send_suggestion_to_ha

asyncio.run(send_suggestion_to_ha(
    suggestion="Test suggestion from Life Ops",
    priority="MEDIUM",
    binding_id="test_123",
    ha_url="http://homeassistant.local:8123"
))

# Check HA notification on phone/glasses
```

### 3. Test Full Loop

```bash
# 1. Send event to Life Ops
# 2. Trigger pattern detection
# 3. Life Ops sends suggestion to HA
# 4. Accept via phone notification
# 5. Check Life Ops logs for acceptance
```

---

## Troubleshooting

### Events Not Appearing in Life Timeline

- Check Life Ops logs: `tail -f logs/orchestrator.log`
- Verify endpoint is accessible: `curl http://<LIFEOPS_IP>:8080/health`
- Check HA automation traces in HA UI

### Suggestions Not Appearing in HA

- Verify webhook URL is correct
- Check HA logs: Settings → System → Logs
- Test webhook manually with curl

### MQTT Connection Issues

- Verify broker is running: `mosquitto -v`
- Check credentials in both HA and Life Ops
- Test with MQTT client: `mosquitto_sub -h localhost -t "lifeops/#"`

### Notifications Not on Glasses

- Ensure glasses are paired and connected
- Check notification settings for HA Companion App
- Test with regular phone notification first

---

## Security Considerations

### For Local Network Only

- Use firewall rules to restrict Life Ops API to local network
- Use strong MQTT passwords
- Consider VPN if accessing remotely

### For Internet-Exposed Setup

- **Required**:
  - Add authentication to Life Ops API (API keys or JWT)
  - Use HTTPS/TLS for all endpoints
  - Use MQTT over TLS
  - Restrict CORS in FastAPI
  
- **Recommended**:
  - Use Home Assistant Cloud or Nabu Casa for secure remote access
  - Implement rate limiting
  - Log all API access
  - Encrypt Life Timeline database

---

## Next Steps

1. **Start Simple**: Implement REST API bridge for one event type (presence)
2. **Add More Events**: Gradually add room sensors, doors, climate
3. **Enable Suggestions**: Start with safety alerts, then add focus/habit suggestions
4. **Close the Loop**: Implement user response handling
5. **Add Automation**: Let Life Ops trigger HA actions (with safeguards)
6. **Optimize**: Switch to MQTT for high-frequency sensors

---

## Advanced: Device-Specific Integrations

### Fitbit via Home Assistant

If using Fitbit integration in HA:

```yaml
automation:
  - id: lifeops_fitbit_sleep
    alias: "Life Ops: Fitbit Sleep"
    trigger:
      - platform: state
        entity_id: sensor.fitbit_sleep_score
    action:
      - service: rest_command.lifeops_event
        data:
          event_type: "sleep"
          features:
            score: "{{ states('sensor.fitbit_sleep_score') }}"
            duration: "{{ states('sensor.fitbit_sleep_duration') }}"
```

### Smart Lights for Focus Mode

```yaml
automation:
  - id: lifeops_focus_mode
    alias: "Life Ops: Focus Mode Activated"
    trigger:
      - platform: webhook
        webhook_id: lifeops-suggestions-webhook
    condition:
      - condition: template
        value_template: "{{ trigger.json.type == 'focus_block' }}"
    action:
      - service: scene.turn_on
        target:
          entity_id: scene.focus_mode
      - service: input_boolean.turn_on
        target:
          entity_id: input_boolean.focus_active
```

---

## Resources

- [Home Assistant REST API](https://developers.home-assistant.io/docs/api/rest/)
- [Home Assistant MQTT](https://www.home-assistant.io/integrations/mqtt/)
- [Home Assistant Webhooks](https://www.home-assistant.io/docs/automation/trigger/#webhook-trigger)
- [Meta Ray-Ban Display](https://www.meta.com/smart-glasses/)
- [Singularis Life Ops Documentation](./README.md)

---

**Questions?** Open an issue or check the Singularis Discord.
