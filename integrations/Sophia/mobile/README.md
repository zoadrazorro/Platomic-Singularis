# Sophia Mobile - Android Life Examination App

> *"Know thyself"* — Delphic maxim

Native Android app for examining your life through conversations with Singularis AGI.

---

## Features

### 1. Conversational Interface
- **Chat with Sophia**: Ask questions about your life in natural language
- **Voice Input**: Speak your questions (Android speech-to-text)
- **Voice Output**: Sophia speaks answers back (text-to-speech)
- **Context-Aware**: Sophia remembers conversation history

### 2. Life Timeline
- Scrollable timeline of all life events
- Filter by date, type, source
- Tap events for details
- Visual density indicators

### 3. Pattern Insights
- Daily/weekly pattern cards
- Habit streaks
- Anomaly alerts with notifications
- Correlation discoveries

### 4. Health Dashboard
- Fitbit metrics visualization
- Sleep quality trends
- Activity vs rest balance
- Heart rate monitoring

### 5. Quick Actions
- "How did I sleep last night?"
- "What patterns do you see this week?"
- "Am I exercising enough?"
- "Show me my room activity"
- Custom queries

### 6. Notifications
- Critical anomaly alerts (falls, no movement)
- Pattern discoveries
- Daily summaries
- Habit reminders

---

## Tech Stack

- **React Native + Expo**: Cross-platform (Android focus)
- **TypeScript**: Type safety
- **React Query**: Data fetching & caching
- **Zustand**: State management
- **React Native Paper**: Material Design UI
- **Victory Native**: Charts
- **Expo Speech**: Voice input/output
- **Expo Notifications**: Push notifications

---

## Setup

### Prerequisites

```bash
# Install Node.js 18+
# Install Expo CLI
npm install -g expo-cli

# Install Android Studio (for emulator)
# Or use physical Android device
```

### Installation

```bash
cd integrations/Sophia/mobile

# Install dependencies
npm install

# Start development server
npx expo start

# Run on Android
# Press 'a' for Android emulator
# Or scan QR code with Expo Go app on physical device
```

### Configuration

Create `.env`:

```bash
# Sophia API (must be accessible from phone)
EXPO_PUBLIC_API_URL=http://192.168.1.100:8081

# Or use ngrok for testing
# EXPO_PUBLIC_API_URL=https://your-ngrok-url.ngrok.io

# User ID
EXPO_PUBLIC_USER_ID=main_user
```

---

## Project Structure

```
mobile/
├── app/                    # Expo Router pages
│   ├── (tabs)/            # Tab navigation
│   │   ├── index.tsx      # Chat screen
│   │   ├── timeline.tsx   # Timeline view
│   │   ├── patterns.tsx   # Patterns dashboard
│   │   └── health.tsx     # Health metrics
│   ├── _layout.tsx        # Root layout
│   └── +not-found.tsx     # 404 page
├── components/            # Reusable components
│   ├── chat/
│   │   ├── ChatBubble.tsx
│   │   ├── VoiceButton.tsx
│   │   └── QuickActions.tsx
│   ├── timeline/
│   │   ├── EventCard.tsx
│   │   └── TimelineView.tsx
│   ├── patterns/
│   │   ├── PatternCard.tsx
│   │   └── AnomalyAlert.tsx
│   └── health/
│       ├── MetricChart.tsx
│       └── HealthSummary.tsx
├── services/              # API & business logic
│   ├── api.ts            # Sophia API client
│   ├── chat.ts           # Chat service
│   └── notifications.ts  # Push notifications
├── stores/               # Zustand stores
│   ├── chatStore.ts
│   ├── timelineStore.ts
│   └── userStore.ts
├── types/                # TypeScript types
│   └── index.ts
├── constants/            # App constants
│   └── Colors.ts
├── app.json             # Expo config
├── package.json
└── tsconfig.json
```

---

## Screens

### 1. Chat Screen (Home)

**Layout**:
```
┌─────────────────────────────────┐
│  Sophia 🦉                      │
├─────────────────────────────────┤
│                                 │
│  [User] How did I sleep?        │
│                                 │
│  [Sophia] You slept 7.5 hours   │
│  last night with 85% quality... │
│                                 │
│  [User] What about exercise?    │
│                                 │
│  [Sophia] You haven't exercised │
│  in 3 days. Would you like...   │
│                                 │
├─────────────────────────────────┤
│ [🎤] [Type message...] [Send]   │
└─────────────────────────────────┘
```

**Features**:
- Chat bubbles with timestamps
- Voice input button (hold to speak)
- Quick action chips above keyboard
- Auto-scroll to latest message
- Loading indicators for AGI responses

### 2. Timeline Screen

**Layout**:
```
┌─────────────────────────────────┐
│  Timeline                       │
│  [Filter] [Date Picker]         │
├─────────────────────────────────┤
│                                 │
│  Today                          │
│  ├─ 08:00 🏠 Arrived Home       │
│  ├─ 09:30 💤 Sleep (7.5h)       │
│  ├─ 14:00 🚪 Door Open          │
│  └─ 18:00 🏃 Exercise (30min)   │
│                                 │
│  Yesterday                      │
│  ├─ 07:00 🏠 Left Home          │
│  ├─ 12:00 💬 Message            │
│  └─ 22:00 💤 Sleep (8h)         │
│                                 │
└─────────────────────────────────┘
```

**Features**:
- Grouped by day
- Icon per event type
- Swipe to see details
- Pull to refresh
- Infinite scroll

### 3. Patterns Screen

**Layout**:
```
┌─────────────────────────────────┐
│  Patterns & Insights            │
├─────────────────────────────────┤
│                                 │
│  ⚠️ ANOMALY ALERT               │
│  No movement for 6 hours        │
│  [Dismiss] [Details]            │
│                                 │
│  🔥 Habit Streak                │
│  Exercise: 7 days               │
│  Keep it up!                    │
│                                 │
│  📊 Correlation Found           │
│  Exercise → Better Sleep        │
│  +15% quality improvement       │
│                                 │
└─────────────────────────────────┘
```

**Features**:
- Pattern cards with confidence scores
- Anomaly alerts (dismissible)
- Tap for detailed analysis
- Share insights

### 4. Health Screen

**Layout**:
```
┌─────────────────────────────────┐
│  Health Metrics                 │
├─────────────────────────────────┤
│                                 │
│  Sleep Quality (7 days)         │
│  [Line chart]                   │
│  Avg: 82% | Best: 95%           │
│                                 │
│  Heart Rate (Today)             │
│  [Area chart]                   │
│  Resting: 62 bpm                │
│                                 │
│  Activity                       │
│  Steps: 8,432 | Goal: 10,000    │
│  [Progress bar]                 │
│                                 │
└─────────────────────────────────┘
```

**Features**:
- Interactive charts (pinch to zoom)
- Time range selector
- Export data
- Set goals

---

## Conversational AI Integration

### Chat Flow

```typescript
// User asks question
const response = await sophiaAPI.chat({
  user_id: 'main_user',
  message: 'How did I sleep last night?',
  conversation_history: previousMessages
});

// Sophia processes via:
// 1. Sophia API receives message
// 2. Queries LifeTimeline for relevant data
// 3. Sends to Singularis consciousness layer
// 4. Gets AGI-generated response
// 5. Returns to mobile app

// App displays response
addMessage({
  role: 'assistant',
  content: response.answer,
  timestamp: new Date()
});
```

### Voice Interaction

```typescript
// Voice input
import * as Speech from 'expo-speech';

// Start listening
const { transcript } = await Speech.recognizeAsync({
  language: 'en-US'
});

// Send to Sophia
const response = await sophiaAPI.chat({
  message: transcript,
  ...
});

// Speak response
Speech.speak(response.answer, {
  language: 'en-US',
  pitch: 1.0,
  rate: 0.9
});
```

### Quick Actions

Pre-defined queries for common questions:

```typescript
const quickActions = [
  { label: '💤 Sleep', query: 'How did I sleep last night?' },
  { label: '🏃 Exercise', query: 'Am I exercising enough?' },
  { label: '📊 Patterns', query: 'What patterns do you see this week?' },
  { label: '🏠 Home', query: 'How much time did I spend at home?' },
  { label: '❤️ Health', query: 'How is my health trending?' },
];
```

---

## API Endpoints Used

### Chat Endpoint (New)

Add to `sophia_api.py`:

```python
@app.post("/chat")
async def chat_with_sophia(
    user_id: str,
    message: str,
    conversation_history: Optional[List[Dict]] = None
):
    """
    Chat with Sophia about your life.
    
    Integrates with LifeQueryHandler and Singularis consciousness.
    """
    # Get relevant context from timeline
    recent_events = timeline.query_by_time(
        user_id,
        datetime.now() - timedelta(days=7),
        datetime.now()
    )
    
    # Build context
    context = f"Recent events: {len(recent_events)}\n"
    # ... add more context
    
    # Query consciousness layer (via LifeQueryHandler)
    if life_query_handler:
        result = await life_query_handler.handle_query(user_id, message)
        response = result.response
        confidence = result.confidence
    else:
        # Fallback
        response = "I'm still learning. Try asking about specific events or patterns."
        confidence = 0.5
    
    return {
        'answer': response,
        'confidence': confidence,
        'sources': ['timeline', 'patterns', 'consciousness'],
        'timestamp': datetime.now().isoformat()
    }
```

### Timeline Endpoints
- `GET /timeline/events?days=7`
- `GET /timeline/summary?days=7`

### Pattern Endpoints
- `GET /patterns/all`
- `GET /patterns/anomalies`

### Health Endpoints
- `GET /health/summary?days=7`

---

## Building for Android

### Development Build

```bash
# Create development build
npx expo prebuild --platform android

# Run on device
npx expo run:android
```

### Production Build

```bash
# Configure app.json
{
  "expo": {
    "name": "Sophia",
    "slug": "sophia-life-examination",
    "version": "1.0.0",
    "android": {
      "package": "com.singularis.sophia",
      "versionCode": 1,
      "permissions": [
        "RECORD_AUDIO",
        "NOTIFICATIONS"
      ]
    }
  }
}

# Build APK
eas build --platform android --profile production

# Or build locally
npx expo build:android
```

### Install on Device

```bash
# Via USB
adb install sophia.apk

# Or share APK file directly
```

---

## Notifications

### Setup Push Notifications

```typescript
// Register for notifications
import * as Notifications from 'expo-notifications';

const { status } = await Notifications.requestPermissionsAsync();

// Get push token
const token = await Notifications.getExpoPushTokenAsync();

// Send to Sophia API to register
await sophiaAPI.registerDevice({
  user_id: 'main_user',
  push_token: token.data,
  platform: 'android'
});
```

### Notification Types

1. **Critical Alerts**: Falls, no movement (immediate)
2. **Pattern Discoveries**: New habits, correlations (daily digest)
3. **Daily Summary**: End-of-day recap (9 PM)
4. **Reminders**: Based on patterns (e.g., "Time for your walk?")

---

## Offline Support

### Local Caching

```typescript
// React Query with persistence
import { QueryClient } from '@tanstack/react-query';
import AsyncStorage from '@react-native-async-storage/async-storage';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      cacheTime: 1000 * 60 * 60 * 24, // 24 hours
      staleTime: 1000 * 60 * 5, // 5 minutes
    },
  },
});

// Persist to AsyncStorage
import { persistQueryClient } from '@tanstack/react-query-persist-client';

persistQueryClient({
  queryClient,
  persister: createAsyncStoragePersister({ storage: AsyncStorage }),
});
```

### Offline Chat

- Queue messages when offline
- Sync when connection restored
- Show offline indicator
- Cache recent conversations

---

## Privacy & Security

### Data Protection

- All data fetched from local Sophia API (no cloud)
- Conversations stored locally on device
- Optional: Encrypt AsyncStorage with device keychain
- No analytics or tracking

### Network Security

```typescript
// Use HTTPS in production
const API_URL = __DEV__ 
  ? 'http://192.168.1.100:8081'  // Local dev
  : 'https://sophia.yourdomain.com';  // Production

// Add API key authentication
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Authorization': `Bearer ${API_KEY}`
  }
});
```

---

## Example Conversations

### Sleep Analysis
```
You: How did I sleep last night?

Sophia: You slept 7.5 hours with 85% quality. Your deep 
sleep was 2.1 hours, which is excellent. You went to bed 
at 10:30 PM and woke at 6:00 AM.

You: Is that better than usual?

Sophia: Yes! Your average sleep quality this week is 78%, 
so last night was 7% above average. You've been sleeping 
better since you started exercising regularly.
```

### Pattern Discovery
```
You: What patterns do you see this week?

Sophia: I've noticed 3 interesting patterns:

1. 🏃 Exercise Habit: You've exercised 5 days this week, 
   always between 5-7 PM. Keep it up!

2. 💤 Sleep Correlation: On days you exercise, your sleep 
   quality improves by 15% on average.

3. 🏠 Room Activity: You spend 80% of your time in the 
   office during work hours (9 AM - 5 PM).

Would you like details on any of these?
```

### Health Check
```
You: Am I healthy?

Sophia: Based on your data:

✅ Sleep: Excellent (avg 7.8h, 82% quality)
✅ Exercise: Good (4-5 days/week)
✅ Heart Rate: Normal (resting 62 bpm)
⚠️ Activity: Could improve (avg 6,500 steps vs 10k goal)

Recommendation: Try adding a 15-minute walk after lunch 
to reach your step goal. Your data shows you're usually 
free around 1 PM.
```

---

## Roadmap

### Phase 1: Core Chat (Week 1)
- [x] Project setup
- [ ] Basic chat UI
- [ ] Sophia API integration
- [ ] Voice input/output
- [ ] Quick actions

### Phase 2: Timeline & Patterns (Week 2)
- [ ] Timeline view
- [ ] Event cards
- [ ] Pattern cards
- [ ] Anomaly alerts

### Phase 3: Health Dashboard (Week 3)
- [ ] Health metrics charts
- [ ] Trend analysis
- [ ] Goal tracking

### Phase 4: Notifications (Week 4)
- [ ] Push notification setup
- [ ] Critical alerts
- [ ] Daily summaries
- [ ] Pattern discoveries

### Phase 5: Polish (Week 5)
- [ ] Offline support
- [ ] Performance optimization
- [ ] Dark mode
- [ ] Animations
- [ ] Production build

---

## Development Commands

```bash
# Start development server
npm start

# Run on Android emulator
npm run android

# Run on physical device
# Scan QR code with Expo Go app

# Type checking
npm run type-check

# Linting
npm run lint

# Tests
npm test

# Build production APK
npm run build:android
```

---

## Troubleshooting

### Can't Connect to API

```bash
# Check API is running
curl http://192.168.1.100:8081/health

# Check phone and computer on same network
# Use ngrok for testing:
ngrok http 8081
# Update EXPO_PUBLIC_API_URL to ngrok URL
```

### Voice Not Working

- Check microphone permissions in Android settings
- Ensure device has Google Speech Services installed
- Test with `expo-speech` example

### Notifications Not Appearing

- Check notification permissions
- Verify Expo push token registration
- Test with Expo push notification tool

---

## Resources

- [Expo Documentation](https://docs.expo.dev/)
- [React Native Paper](https://callstack.github.io/react-native-paper/)
- [React Query](https://tanstack.com/query/latest)
- [Expo Speech](https://docs.expo.dev/versions/latest/sdk/speech/)
- [Victory Native](https://formidable.com/open-source/victory/docs/native/)

---

**Sophia Mobile**: Examine your life, anytime, anywhere. 🦉📱
