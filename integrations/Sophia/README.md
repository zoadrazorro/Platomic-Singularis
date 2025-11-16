# Sophia - Life Examination Dashboard

> *"The unexamined life is not worth living."* — Socrates

Sophia is a visualization and analysis app for the LifeOps stack. It transforms your life data into insights, patterns, and self-knowledge.

---

## Philosophy

Named after the Greek word for wisdom (σοφία), Sophia embodies the Socratic principle that self-examination is essential to a meaningful life. Rather than passively collecting data, Sophia helps you actively reflect on:

- **Patterns**: What recurring themes shape your days?
- **Anomalies**: When do you deviate from your norms, and why?
- **Correlations**: How do different aspects of your life influence each other?
- **Trends**: Are you moving toward your goals or drifting?
- **Meaning**: What does the data reveal about your values and priorities?

---

## Features

### 1. Life Timeline Visualization
- Interactive timeline of all life events
- Filter by source, type, date range
- Zoom from years → months → days → hours
- Event details on hover/click

### 2. Pattern Dashboard
- Detected patterns from Pattern Engine
- Habit streaks and consistency metrics
- Correlation heatmaps (sleep vs exercise, etc.)
- Anomaly alerts with context

### 3. Health & Wellness
- Fitbit metrics over time (HR, sleep, steps)
- Energy levels and recovery trends
- Activity vs rest balance
- Safety alerts (falls, no movement)

### 4. Context Awareness
- Room occupancy heatmaps
- Home/away patterns
- Time-of-day activity distribution
- Social interaction frequency

### 5. AGI Insights
- Natural language summaries of periods
- "Ask Sophia" query interface
- Suggested focus areas for improvement
- Philosophical reflections on your data

### 6. Temporal Analysis
- Day/week/month comparisons
- Best/worst periods identification
- Seasonal patterns
- Long-term trend projections

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│                   Sophia Web UI                 │
│              (React + D3.js + Recharts)         │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│              Sophia API (FastAPI)               │
│  - /timeline/events                             │
│  - /patterns/all                                │
│  - /health/summary                              │
│  - /insights/query                              │
│  - /visualizations/data                         │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│              LifeOps Core Stack                 │
│  - LifeTimeline (SQLite)                        │
│  - PatternEngine                                │
│  - LifeQueryHandler                             │
│  - UnifiedConsciousnessLayer                    │
└─────────────────────────────────────────────────┘
```

---

## Tech Stack

### Backend
- **FastAPI**: REST API server
- **SQLite**: Direct access to LifeTimeline
- **Pandas**: Data aggregation and analysis
- **Plotly**: Server-side chart generation

### Frontend
- **React**: UI framework
- **D3.js**: Custom visualizations
- **Recharts**: Standard charts
- **TailwindCSS**: Styling
- **React Query**: Data fetching

---

## Quick Start

### 1. Install Dependencies

```bash
cd integrations/Sophia
pip install -r requirements.txt
cd frontend
npm install
```

### 2. Start Backend

```bash
# From integrations/Sophia
python sophia_api.py
# Runs on http://localhost:8081
```

### 3. Start Frontend

```bash
cd frontend
npm start
# Opens http://localhost:3000
```

### 4. Access Sophia

Navigate to `http://localhost:3000` and start examining your life.

---

## Usage Examples

### View Timeline

```bash
# Get events for last 7 days
curl http://localhost:8081/timeline/events?days=7

# Get specific event types
curl http://localhost:8081/timeline/events?type=sleep&days=30
```

### Query Patterns

```bash
# Get all detected patterns
curl http://localhost:8081/patterns/all?user_id=main_user

# Get specific pattern type
curl http://localhost:8081/patterns/habits?user_id=main_user
```

### Ask Questions

```bash
# Natural language query
curl -X POST http://localhost:8081/insights/query \
  -H "Content-Type: application/json" \
  -d '{"user_id":"main_user","query":"How did I sleep this week?"}'
```

---

## Visualization Types

### 1. Timeline View
- Horizontal scrollable timeline
- Color-coded by event type
- Density indicators for busy periods
- Click to see event details

### 2. Heatmaps
- **Room Occupancy**: Which rooms, when
- **Activity Levels**: Hour-by-hour energy
- **Correlation Matrix**: Variable relationships

### 3. Trend Charts
- Line charts for continuous metrics (HR, steps)
- Bar charts for discrete events (exercises, meals)
- Area charts for cumulative totals

### 4. Pattern Cards
- Visual cards for each detected pattern
- Confidence scores
- Evidence timeline
- Recommendations

### 5. Anomaly Alerts
- Red flags for critical events
- Context and severity
- Historical comparison
- Suggested actions

---

## Configuration

Create `.env` in `integrations/Sophia`:

```bash
# LifeOps Connection
LIFEOPS_DB_PATH=../../data/life_timeline.db
LIFEOPS_API_URL=http://localhost:8080

# Sophia API
SOPHIA_PORT=8081
SOPHIA_HOST=0.0.0.0

# AGI Features
ENABLE_AGI_INSIGHTS=true
OPENAI_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here

# UI Preferences
DEFAULT_USER_ID=main_user
DEFAULT_DAYS_BACK=7
THEME=dark  # or light
```

---

## API Reference

### Timeline Endpoints

- `GET /timeline/events` - Get life events
  - Query params: `user_id`, `days`, `type`, `source`, `start`, `end`
  
- `GET /timeline/summary` - Get summary statistics
  - Query params: `user_id`, `days`

- `GET /timeline/day/{date}` - Get specific day's events

### Pattern Endpoints

- `GET /patterns/all` - All detected patterns
- `GET /patterns/habits` - Habit patterns only
- `GET /patterns/correlations` - Correlation patterns
- `GET /patterns/anomalies` - Anomalies and alerts

### Health Endpoints

- `GET /health/summary` - Health metrics summary
- `GET /health/sleep` - Sleep analysis
- `GET /health/activity` - Activity metrics
- `GET /health/trends` - Long-term trends

### Insight Endpoints

- `POST /insights/query` - Natural language query
- `GET /insights/daily` - Daily summary
- `GET /insights/weekly` - Weekly summary
- `GET /insights/recommendations` - Improvement suggestions

### Visualization Endpoints

- `GET /viz/timeline` - Timeline data for D3
- `GET /viz/heatmap` - Heatmap data
- `GET /viz/trends` - Trend chart data
- `GET /viz/correlations` - Correlation matrix

---

## Development Roadmap

### Phase 1: Core Visualization (Week 1)
- [x] Project structure
- [ ] FastAPI backend with timeline access
- [ ] React frontend scaffold
- [ ] Basic timeline visualization
- [ ] Event detail views

### Phase 2: Pattern Display (Week 2)
- [ ] Pattern cards UI
- [ ] Habit streak visualization
- [ ] Anomaly alerts
- [ ] Correlation heatmaps

### Phase 3: Health Dashboard (Week 3)
- [ ] Fitbit metrics charts
- [ ] Sleep quality analysis
- [ ] Activity vs rest balance
- [ ] Energy level tracking

### Phase 4: AGI Integration (Week 4)
- [ ] Natural language query interface
- [ ] Daily/weekly summaries
- [ ] Philosophical insights
- [ ] Recommendation engine

### Phase 5: Advanced Features (Week 5+)
- [ ] Export reports (PDF, CSV)
- [ ] Goal tracking
- [ ] Comparative analysis (this week vs last)
- [ ] Predictive insights
- [ ] Mobile responsive design

---

## Design Principles

1. **Clarity over Complexity**: Show insights, not raw data dumps
2. **Context is King**: Every metric needs temporal and situational context
3. **Actionable**: Insights should suggest next steps
4. **Beautiful**: Data visualization as art
5. **Fast**: Sub-second load times, smooth interactions
6. **Private**: All data stays local, no external services (except optional LLM)

---

## Philosophical Foundations

Sophia is built on several philosophical principles:

### Socratic Examination
Self-knowledge through questioning. The app prompts reflection, not passive consumption.

### Stoic Awareness
Focus on what you can control. Sophia highlights patterns you can change.

### Buddhist Mindfulness
Present-moment awareness informed by past patterns. See where you are, how you got here.

### Spinozist Holism
Everything is connected. Sophia reveals the web of causes and effects in your life.

---

## Privacy & Security

- **Local-First**: All data stored locally in SQLite
- **No Tracking**: No analytics, no telemetry
- **Optional Cloud**: LLM features are opt-in
- **Export Control**: You own your data, export anytime
- **Encryption**: Optional database encryption

---

## Contributing

Sophia is part of the Singularis project. Contributions welcome:

1. Visualization improvements
2. New pattern detectors
3. UI/UX enhancements
4. Documentation
5. Philosophical insights integration

---

## Quotes to Inspire

> *"Know thyself."* — Delphic maxim

> *"The unexamined life is not worth living."* — Socrates

> *"We cannot change what we are not aware of."* — Sheryl Sandberg

> *"What gets measured gets managed."* — Peter Drucker

> *"The greatest thing in the world is to know how to belong to oneself."* — Michel de Montaigne

---

## License

MIT License - Part of the Singularis project

---

**Sophia**: Wisdom through self-examination. 🦉
