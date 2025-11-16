# Sophia Mobile - Quick Start Guide

Get the Sophia Android app running in 10 minutes.

---

## Prerequisites

1. **Node.js 18+** installed
2. **Android device** or **Android Studio emulator**
3. **Sophia API running** (see backend setup below)

---

## Step 1: Start Sophia API Backend

```bash
# Terminal 1 - Start Sophia API
cd integrations/Sophia
pip install -r requirements.txt
python sophia_api.py

# Should see:
# [SOPHIA] Starting on 0.0.0.0:8081
# [SOPHIA] Connected to LifeTimeline
```

---

## Step 2: Get Your Local IP Address

**Windows**:
```powershell
ipconfig
# Look for "IPv4 Address" under your active network adapter
# Example: 192.168.1.100
```

**Mac/Linux**:
```bash
ifconfig | grep "inet "
# Example: 192.168.1.100
```

---

## Step 3: Setup Mobile App

```bash
# Terminal 2 - Setup mobile app
cd integrations/Sophia/mobile

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Edit .env with your IP address
# EXPO_PUBLIC_API_URL=http://192.168.1.100:8081
```

---

## Step 4: Run on Android

### Option A: Physical Device (Recommended)

1. **Install Expo Go** on your Android phone from Play Store
2. **Enable Developer Mode** on your phone:
   - Settings → About Phone → Tap "Build Number" 7 times
   - Settings → Developer Options → Enable "USB Debugging"
3. **Connect phone to computer** via USB
4. **Start Expo**:
   ```bash
   npm start
   ```
5. **Press 'a'** to open on Android device

### Option B: Android Emulator

1. **Install Android Studio**
2. **Create AVD** (Android Virtual Device):
   - Tools → AVD Manager → Create Virtual Device
   - Choose Pixel 5 or similar
   - Download system image (API 33+)
3. **Start emulator** from AVD Manager
4. **Start Expo**:
   ```bash
   npm start
   # Press 'a' for Android
   ```

### Option C: Expo Go App (Easiest)

1. **Install Expo Go** from Play Store
2. **Start Expo**:
   ```bash
   npm start
   ```
3. **Scan QR code** with Expo Go app
4. **Make sure phone and computer are on same WiFi**

---

## Step 5: Test Chat

Once the app opens:

1. You'll see the **Chat screen** with Sophia 🦉
2. Try these questions:
   - "How did I sleep last night?"
   - "What patterns do you see?"
   - "Am I exercising enough?"
3. Tap the **🎤 microphone** to use voice input

---

## Troubleshooting

### Can't Connect to API

**Problem**: "Network Error" or "Failed to fetch"

**Solution**:
```bash
# 1. Check API is running
curl http://localhost:8081/health

# 2. Check from phone's perspective
# Replace with your IP
curl http://192.168.1.100:8081/health

# 3. If still failing, use ngrok:
ngrok http 8081
# Update .env with ngrok URL:
# EXPO_PUBLIC_API_URL=https://abc123.ngrok.io
```

### App Won't Load

**Problem**: Metro bundler errors

**Solution**:
```bash
# Clear cache and restart
npm start -- --clear

# Or reset completely
rm -rf node_modules
npm install
npm start
```

### Voice Not Working

**Problem**: Microphone button doesn't work

**Solution**:
- Check microphone permissions in Android settings
- Ensure Google Speech Services is installed
- Try typing first to verify API connection

---

## Next Steps

### Add Some Test Data

```bash
# Add test events to timeline
curl -X POST http://localhost:8081/ha/event \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "main_user",
    "source": "manual",
    "event_type": "sleep",
    "features": {"duration_hours": 7.5, "quality": 0.85}
  }'

# Now ask Sophia: "How did I sleep?"
```

### Explore Other Screens

- Swipe or tap tabs to see:
  - **Timeline**: All your life events
  - **Patterns**: Detected habits and correlations
  - **Health**: Metrics and trends

### Enable Notifications

```bash
# In app, grant notification permissions when prompted
# Critical alerts will appear as push notifications
```

---

## Development Tips

### Hot Reload

- Save any file in `app/` or `components/`
- App automatically reloads on device
- Shake device to open developer menu

### Debug Console

```bash
# View logs in terminal where you ran npm start
# Or shake device → "Debug Remote JS"
```

### Test API Endpoints

```bash
# Get timeline
curl http://192.168.1.100:8081/timeline/events?days=7

# Chat
curl -X POST http://192.168.1.100:8081/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id":"main_user","message":"Hello Sophia"}'

# Patterns
curl http://192.168.1.100:8081/patterns/all?user_id=main_user
```

---

## Building APK

When ready to install permanently on device:

```bash
# Install EAS CLI
npm install -g eas-cli

# Login to Expo
eas login

# Build APK
eas build --platform android --profile preview

# Download and install APK on device
```

---

## What's Next?

- **Integrate with Home Assistant** (see `HA_INTEGRATION.md`)
- **Add Fitbit data** for richer health insights
- **Enable camera feeds** for room activity tracking
- **Customize quick actions** in the chat screen
- **Set up daily summaries** as notifications

---

**You're ready to examine your life with Sophia!** 🦉📱

Questions? Check the main README or open an issue.
