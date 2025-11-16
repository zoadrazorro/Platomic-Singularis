"""
Sophia API - Life Examination Dashboard Backend

FastAPI server providing endpoints for visualizing and analyzing LifeOps data.

"The unexamined life is not worth living." - Socrates
"""

import os
import sys
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import uvicorn

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from life_timeline import LifeTimeline, EventSource, EventType
from pattern_engine import PatternEngine

# Initialize FastAPI
app = FastAPI(
    title="Sophia - Life Examination API",
    description="Wisdom through self-examination",
    version="1.0.0"
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
timeline: Optional[LifeTimeline] = None
pattern_engine: Optional[PatternEngine] = None
config = {
    'db_path': os.getenv('LIFEOPS_DB_PATH', '../data/life_timeline.db'),
    'default_user_id': os.getenv('DEFAULT_USER_ID', 'main_user'),
    'default_days_back': int(os.getenv('DEFAULT_DAYS_BACK', '7')),
}


@app.on_event("startup")
async def startup():
    """Initialize Sophia on startup."""
    global timeline, pattern_engine
    
    logger.info("[SOPHIA] Starting Life Examination Dashboard...")
    
    # Initialize timeline
    db_path = config['db_path']
    if not Path(db_path).exists():
        logger.warning(f"[SOPHIA] Database not found at {db_path}, creating new one")
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    
    timeline = LifeTimeline(db_path)
    logger.info(f"[SOPHIA] Connected to LifeTimeline: {db_path}")
    
    # Initialize pattern engine
    pattern_engine = PatternEngine(timeline)
    logger.info("[SOPHIA] Pattern Engine initialized")
    
    logger.info("[SOPHIA] ✅ Sophia is ready to examine your life")


# ============================================================================
# Timeline Endpoints
# ============================================================================

@app.get("/timeline/events")
async def get_timeline_events(
    user_id: str = Query(default=None),
    days: int = Query(default=7, ge=1, le=365),
    event_type: Optional[str] = None,
    source: Optional[str] = None,
    start: Optional[str] = None,
    end: Optional[str] = None
):
    """
    Get life events from timeline.
    
    Query params:
    - user_id: User ID (default from config)
    - days: Days back from now (default 7)
    - event_type: Filter by event type
    - source: Filter by source
    - start: Start datetime (ISO format)
    - end: End datetime (ISO format)
    """
    if not timeline:
        raise HTTPException(status_code=500, detail="Timeline not initialized")
    
    user_id = user_id or config['default_user_id']
    
    # Parse time range
    if start and end:
        start_dt = datetime.fromisoformat(start)
        end_dt = datetime.fromisoformat(end)
    else:
        end_dt = datetime.now()
        start_dt = end_dt - timedelta(days=days)
    
    # Parse filters
    evt_type = EventType(event_type) if event_type else None
    evt_source = EventSource(source) if source else None
    
    # Query timeline
    events = timeline.query_by_time(
        user_id,
        start_dt,
        end_dt,
        event_type=evt_type,
        source=evt_source
    )
    
    # Convert to dicts
    events_data = [e.to_dict() for e in events]
    
    return {
        'events': events_data,
        'count': len(events_data),
        'start': start_dt.isoformat(),
        'end': end_dt.isoformat(),
        'user_id': user_id
    }


@app.get("/timeline/summary")
async def get_timeline_summary(
    user_id: str = Query(default=None),
    days: int = Query(default=7, ge=1, le=365)
):
    """Get summary statistics for time period."""
    if not timeline:
        raise HTTPException(status_code=500, detail="Timeline not initialized")
    
    user_id = user_id or config['default_user_id']
    
    summary = timeline.get_timeline_summary(user_id, days)
    
    return {
        'summary': summary,
        'user_id': user_id
    }


@app.get("/timeline/day/{date}")
async def get_day_events(
    date: str,
    user_id: str = Query(default=None)
):
    """Get all events for a specific day (YYYY-MM-DD)."""
    if not timeline:
        raise HTTPException(status_code=500, detail="Timeline not initialized")
    
    user_id = user_id or config['default_user_id']
    
    try:
        day = datetime.fromisoformat(date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format (use YYYY-MM-DD)")
    
    events = timeline.query_day(user_id, day)
    events_data = [e.to_dict() for e in events]
    
    return {
        'date': date,
        'events': events_data,
        'count': len(events_data),
        'user_id': user_id
    }


# ============================================================================
# Pattern Endpoints
# ============================================================================

@app.get("/patterns/all")
async def get_all_patterns(
    user_id: str = Query(default=None)
):
    """Get all detected patterns."""
    if not pattern_engine:
        raise HTTPException(status_code=500, detail="Pattern engine not initialized")
    
    user_id = user_id or config['default_user_id']
    
    analysis = pattern_engine.analyze_all(user_id)
    
    return {
        'patterns': analysis.get('patterns', []),
        'anomalies': analysis.get('anomalies', []),
        'alert_level': analysis.get('alert_level'),
        'summary': analysis.get('summary'),
        'timestamp': analysis.get('timestamp'),
        'user_id': user_id
    }


@app.get("/patterns/habits")
async def get_habit_patterns(
    user_id: str = Query(default=None),
    days: int = Query(default=30, ge=7, le=90)
):
    """Get habit patterns."""
    if not pattern_engine:
        raise HTTPException(status_code=500, detail="Pattern engine not initialized")
    
    user_id = user_id or config['default_user_id']
    
    patterns = pattern_engine.detect_habit_patterns(user_id, days=days)
    
    return {
        'habits': [p.__dict__ for p in patterns],
        'count': len(patterns),
        'days_analyzed': days,
        'user_id': user_id
    }


@app.get("/patterns/correlations")
async def get_correlations(
    user_id: str = Query(default=None),
    days: int = Query(default=30, ge=7, le=90)
):
    """Get correlation patterns."""
    if not pattern_engine:
        raise HTTPException(status_code=500, detail="Pattern engine not initialized")
    
    user_id = user_id or config['default_user_id']
    
    patterns = pattern_engine.detect_correlations(user_id, days=days)
    
    return {
        'correlations': [p.__dict__ for p in patterns],
        'count': len(patterns),
        'days_analyzed': days,
        'user_id': user_id
    }


@app.get("/patterns/anomalies")
async def get_anomalies(
    user_id: str = Query(default=None)
):
    """Get current anomalies and alerts."""
    if not pattern_engine:
        raise HTTPException(status_code=500, detail="Pattern engine not initialized")
    
    user_id = user_id or config['default_user_id']
    
    anomalies = []
    
    # Check for various anomalies
    fall = pattern_engine.detect_fall(user_id)
    if fall:
        anomalies.append(fall.__dict__)
    
    no_movement = pattern_engine.detect_no_movement(user_id)
    if no_movement:
        anomalies.append(no_movement.__dict__)
    
    hr_anomaly = pattern_engine.detect_hr_anomaly(user_id)
    if hr_anomaly:
        anomalies.append(hr_anomaly.__dict__)
    
    return {
        'anomalies': anomalies,
        'count': len(anomalies),
        'user_id': user_id,
        'timestamp': datetime.now().isoformat()
    }


# ============================================================================
# Health Endpoints
# ============================================================================

@app.get("/health/summary")
async def get_health_summary(
    user_id: str = Query(default=None),
    days: int = Query(default=7, ge=1, le=30)
):
    """Get health metrics summary."""
    if not timeline:
        raise HTTPException(status_code=500, detail="Timeline not initialized")
    
    user_id = user_id or config['default_user_id']
    
    # Get health events
    end_dt = datetime.now()
    start_dt = end_dt - timedelta(days=days)
    
    health_events = timeline.query_by_time(
        user_id,
        start_dt,
        end_dt,
        source=EventSource.FITBIT
    )
    
    # Aggregate by type
    summary = {
        'sleep': [],
        'heart_rate': [],
        'steps': [],
        'exercise': []
    }
    
    for event in health_events:
        if event.type == EventType.SLEEP:
            summary['sleep'].append({
                'timestamp': event.timestamp.isoformat(),
                'duration': event.features.get('duration_hours', 0),
                'quality': event.features.get('quality', 0)
            })
        elif event.type == EventType.HEART_RATE:
            summary['heart_rate'].append({
                'timestamp': event.timestamp.isoformat(),
                'bpm': event.features.get('bpm', 0)
            })
        elif event.type == EventType.STEPS:
            summary['steps'].append({
                'timestamp': event.timestamp.isoformat(),
                'count': event.features.get('count', 0)
            })
        elif event.type == EventType.EXERCISE:
            summary['exercise'].append({
                'timestamp': event.timestamp.isoformat(),
                'type': event.features.get('type', 'unknown'),
                'duration': event.features.get('duration_min', 0)
            })
    
    return {
        'summary': summary,
        'days': days,
        'user_id': user_id
    }


# ============================================================================
# Chat & Insight Endpoints
# ============================================================================

@app.post("/chat")
async def chat_with_sophia(
    user_id: str,
    message: str,
    conversation_history: Optional[List[Dict[str, Any]]] = None
):
    """
    Chat with Sophia about your life.
    
    Integrates with LifeTimeline and pattern detection for context-aware responses.
    """
    if not timeline:
        raise HTTPException(status_code=500, detail="Timeline not initialized")
    
    logger.info(f"[SOPHIA-CHAT] User {user_id}: {message}")
    
    # Get recent context (last 7 days)
    end_dt = datetime.now()
    start_dt = end_dt - timedelta(days=7)
    recent_events = timeline.query_by_time(user_id, start_dt, end_dt)
    
    # Build context summary
    event_summary = f"Recent activity (last 7 days): {len(recent_events)} events\n"
    
    # Count by type
    type_counts = {}
    for event in recent_events:
        type_name = event.type.value
        type_counts[type_name] = type_counts.get(type_name, 0) + 1
    
    if type_counts:
        event_summary += "Event breakdown: " + ", ".join([
            f"{t}: {c}" for t, c in sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        ])
    
    # Get patterns if available
    pattern_summary = ""
    if pattern_engine:
        try:
            analysis = pattern_engine.analyze_all(user_id)
            patterns = analysis.get('patterns', [])
            anomalies = analysis.get('anomalies', [])
            
            if patterns:
                pattern_summary = f"\n\nDetected {len(patterns)} patterns"
            if anomalies:
                pattern_summary += f", {len(anomalies)} anomalies"
        except Exception as e:
            logger.warning(f"[SOPHIA-CHAT] Pattern analysis failed: {e}")
    
    # Build full context
    context = f"""You are Sophia, a wise AI assistant helping the user examine their life.

User's recent life data:
{event_summary}
{pattern_summary}

User's question: {message}

Provide a thoughtful, insightful response based on their life data. Be conversational, empathetic, and actionable.
If you notice patterns or correlations, mention them. If data is missing, acknowledge it gracefully.
"""
    
    # Integrate with full AGI consciousness stack
    use_agi = os.getenv('ENABLE_AGI_INSIGHTS', 'false').lower() == 'true'
    
    if use_agi:
        try:
            # Import AGI components
            from singularis.unified_consciousness_layer import UnifiedConsciousnessLayer
            from singularis.core.being_state import BeingState
            
            # Initialize consciousness if not already done
            if not hasattr(chat_with_sophia, '_consciousness'):
                logger.info("[SOPHIA-CHAT] Initializing full AGI consciousness stack...")
                chat_with_sophia._consciousness = UnifiedConsciousnessLayer()
                
                # Connect to timeline
                if timeline:
                    chat_with_sophia._consciousness.connect_life_timeline(timeline)
                    logger.info("[SOPHIA-CHAT] ✅ AGI consciousness connected to Life Timeline")
            
            consciousness = chat_with_sophia._consciousness
            
            # Build being state from recent events
            being_state = BeingState()
            being_state.update_subsystem('life_context', {
                'recent_events': len(recent_events),
                'event_summary': event_summary,
                'pattern_summary': pattern_summary,
                'conversation_history': len(conversation_history or []),
            })
            
            # Process with full AGI consciousness
            logger.info("[SOPHIA-CHAT] Processing with full AGI consciousness...")
            result = await consciousness.process_unified(
                query=message,
                context=context,
                being_state=being_state,
                subsystem_data={
                    'user_id': user_id,
                    'source': 'sophia_mobile',
                    'recent_events': [e.to_dict() for e in recent_events[-10:]],  # Last 10 events
                }
            )
            
            response = result.response
            confidence = result.coherence_score
            
            logger.info(f"[SOPHIA-CHAT] AGI response (coherence: {confidence:.3f}): {response[:100]}...")
            
        except Exception as e:
            logger.error(f"[SOPHIA-CHAT] AGI processing failed: {e}")
            logger.info("[SOPHIA-CHAT] Falling back to keyword-based responses")
            use_agi = False
    
    # Fallback: Simple keyword-based responses
    if not use_agi:
        message_lower = message.lower()
        
        if 'sleep' in message_lower:
            sleep_events = [e for e in recent_events if e.type == EventType.SLEEP]
            if sleep_events:
                avg_duration = sum(e.features.get('duration_hours', 0) for e in sleep_events) / len(sleep_events)
                response = f"You've had {len(sleep_events)} sleep sessions in the last week, averaging {avg_duration:.1f} hours per night. "
                if avg_duration >= 7.5:
                    response += "That's excellent! You're getting quality rest."
                elif avg_duration >= 6:
                    response += "That's decent, but you might benefit from an extra 30-60 minutes."
                else:
                    response += "You're not getting enough sleep. Aim for 7-8 hours for optimal health."
            else:
                response = "I don't have sleep data for the past week. Make sure your Fitbit is syncing properly."
        
        elif 'exercise' in message_lower or 'workout' in message_lower:
            exercise_events = [e for e in recent_events if e.type == EventType.EXERCISE]
            if exercise_events:
                response = f"You've exercised {len(exercise_events)} times this week. "
                if len(exercise_events) >= 5:
                    response += "Excellent consistency! Keep up the great work."
                elif len(exercise_events) >= 3:
                    response += "Good job! Try to add one or two more sessions for optimal health."
                else:
                    response += "You could benefit from more regular exercise. Aim for 3-5 sessions per week."
            else:
                response = "I don't see any exercise events this week. Time to get moving!"
        
        elif 'pattern' in message_lower:
            if pattern_engine:
                analysis = pattern_engine.analyze_all(user_id)
                patterns = analysis.get('patterns', [])
                if patterns:
                    response = f"I've detected {len(patterns)} patterns:\n\n"
                    for i, p in enumerate(patterns[:3], 1):
                        response += f"{i}. {p.get('name', 'Pattern')}: {p.get('description', 'No description')}\n"
                else:
                    response = "I haven't detected any strong patterns yet. Keep logging data and I'll find insights!"
            else:
                response = "Pattern detection is not available right now."
        
        elif 'home' in message_lower or 'room' in message_lower:
            room_events = [e for e in recent_events if e.type in [EventType.ROOM_ENTER, EventType.ROOM_EXIT]]
            if room_events:
                rooms = [e.features.get('room') for e in room_events if 'room' in e.features]
                if rooms:
                    from collections import Counter
                    room_counts = Counter(rooms)
                    most_common = room_counts.most_common(3)
                    response = f"You've been most active in: {', '.join([f'{r} ({c} times)' for r, c in most_common])}"
                else:
                    response = f"I see {len(room_events)} room activity events, but no specific room data."
            else:
                response = "I don't have room activity data for this week."
        
        else:
            # Generic response
            response = f"Based on your recent activity:\n\n"
            response += f"• {len(recent_events)} life events recorded\n"
            if type_counts:
                top_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:3]
                response += f"• Most common: {', '.join([t.replace('_', ' ') for t, _ in top_types])}\n"
            response += f"\nAsk me specific questions about sleep, exercise, patterns, or your daily routine!"
    
    logger.info(f"[SOPHIA-CHAT] Response: {response[:100]}...")
    
    return {
        'answer': response,
        'confidence': 0.7,  # Will be from AGI when integrated
        'sources': ['timeline', 'patterns'],
        'context_events': len(recent_events),
        'timestamp': datetime.now().isoformat()
    }


@app.post("/insights/query")
async def query_insights(
    user_id: str,
    query: str
):
    """
    Natural language query about life data.
    
    Alias for /chat endpoint for backward compatibility.
    """
    return await chat_with_sophia(user_id, query)


@app.get("/insights/daily")
async def get_daily_summary(
    user_id: str = Query(default=None),
    date: Optional[str] = None
):
    """Get daily summary."""
    if not timeline:
        raise HTTPException(status_code=500, detail="Timeline not initialized")
    
    user_id = user_id or config['default_user_id']
    
    if date:
        day = datetime.fromisoformat(date)
    else:
        day = datetime.now()
    
    events = timeline.query_day(user_id, day)
    
    # Summarize
    summary = {
        'date': day.strftime('%Y-%m-%d'),
        'total_events': len(events),
        'by_type': {},
        'highlights': []
    }
    
    for event in events:
        type_name = event.type.value
        summary['by_type'][type_name] = summary['by_type'].get(type_name, 0) + 1
    
    return summary


# ============================================================================
# Visualization Data Endpoints
# ============================================================================

@app.get("/viz/timeline")
async def get_timeline_viz_data(
    user_id: str = Query(default=None),
    days: int = Query(default=30, ge=1, le=365)
):
    """Get timeline data formatted for D3.js visualization."""
    if not timeline:
        raise HTTPException(status_code=500, detail="Timeline not initialized")
    
    user_id = user_id or config['default_user_id']
    
    end_dt = datetime.now()
    start_dt = end_dt - timedelta(days=days)
    
    events = timeline.query_by_time(user_id, start_dt, end_dt)
    
    # Format for D3 timeline
    viz_data = []
    for event in events:
        viz_data.append({
            'id': event.id,
            'timestamp': event.timestamp.isoformat(),
            'type': event.type.value,
            'source': event.source.value,
            'label': event.type.value.replace('_', ' ').title(),
            'importance': event.importance,
            'confidence': event.confidence
        })
    
    return {
        'data': viz_data,
        'start': start_dt.isoformat(),
        'end': end_dt.isoformat(),
        'count': len(viz_data)
    }


@app.get("/viz/heatmap")
async def get_heatmap_data(
    user_id: str = Query(default=None),
    days: int = Query(default=30, ge=7, le=90),
    metric: str = Query(default="room_activity")
):
    """Get heatmap data (hour x day grid)."""
    if not timeline:
        raise HTTPException(status_code=500, detail="Timeline not initialized")
    
    user_id = user_id or config['default_user_id']
    
    end_dt = datetime.now()
    start_dt = end_dt - timedelta(days=days)
    
    events = timeline.query_by_time(user_id, start_dt, end_dt)
    
    # Build hour x day matrix
    heatmap = {}
    for event in events:
        day = event.timestamp.strftime('%Y-%m-%d')
        hour = event.timestamp.hour
        
        if day not in heatmap:
            heatmap[day] = {h: 0 for h in range(24)}
        
        heatmap[day][hour] += 1
    
    return {
        'heatmap': heatmap,
        'metric': metric,
        'days': days,
        'user_id': user_id
    }


# ============================================================================
# System Endpoints
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        'name': 'Sophia - Life Examination API',
        'version': '1.0.0',
        'quote': 'The unexamined life is not worth living. - Socrates',
        'status': 'operational',
        'endpoints': {
            'timeline': '/timeline/*',
            'patterns': '/patterns/*',
            'health': '/health/*',
            'insights': '/insights/*',
            'visualizations': '/viz/*'
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        'status': 'healthy',
        'timeline_connected': timeline is not None,
        'pattern_engine_ready': pattern_engine is not None,
        'timestamp': datetime.now().isoformat()
    }


if __name__ == "__main__":
    """Run Sophia API server."""
    port = int(os.getenv('SOPHIA_PORT', '8081'))
    host = os.getenv('SOPHIA_HOST', '0.0.0.0')
    
    logger.info(f"[SOPHIA] Starting on {host}:{port}")
    logger.info("[SOPHIA] 'Know thyself' - Delphic maxim")
    
    uvicorn.run(app, host=host, port=port)
