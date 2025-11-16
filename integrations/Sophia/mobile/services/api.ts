/**
 * Sophia API Client
 * 
 * Handles all communication with the Sophia backend API
 */

import axios from 'axios';

const API_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8081';
const USER_ID = process.env.EXPO_PUBLIC_USER_ID || 'main_user';

const api = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Types
export interface LifeEvent {
  id: string;
  user_id: string;
  timestamp: string;
  source: string;
  type: string;
  features: Record<string, any>;
  confidence: number;
  importance: number;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface ChatResponse {
  answer: string;
  confidence: number;
  sources: string[];
  context_events: number;
  timestamp: string;
}

export interface Pattern {
  id: string;
  name: string;
  description: string;
  confidence: number;
  evidence: string[];
  discovered_at: string;
}

export interface Anomaly {
  id: string;
  event: LifeEvent;
  expected_value: string;
  actual_value: string;
  deviation: number;
  alert_level: string;
  message: string;
}

// API Methods

/**
 * Chat with Sophia
 */
export const chatWithSophia = async (
  message: string,
  conversationHistory?: ChatMessage[]
): Promise<ChatResponse> => {
  const response = await api.post('/chat', {
    user_id: USER_ID,
    message,
    conversation_history: conversationHistory,
  });
  return response.data;
};

/**
 * Get timeline events
 */
export const getTimelineEvents = async (
  days: number = 7,
  eventType?: string,
  source?: string
): Promise<{ events: LifeEvent[]; count: number }> => {
  const response = await api.get('/timeline/events', {
    params: {
      user_id: USER_ID,
      days,
      event_type: eventType,
      source,
    },
  });
  return response.data;
};

/**
 * Get timeline summary
 */
export const getTimelineSummary = async (
  days: number = 7
): Promise<any> => {
  const response = await api.get('/timeline/summary', {
    params: {
      user_id: USER_ID,
      days,
    },
  });
  return response.data;
};

/**
 * Get events for specific day
 */
export const getDayEvents = async (
  date: string
): Promise<{ events: LifeEvent[]; count: number }> => {
  const response = await api.get(`/timeline/day/${date}`, {
    params: {
      user_id: USER_ID,
    },
  });
  return response.data;
};

/**
 * Get all patterns
 */
export const getAllPatterns = async (): Promise<{
  patterns: Pattern[];
  anomalies: Anomaly[];
  alert_level: string;
  summary: string;
}> => {
  const response = await api.get('/patterns/all', {
    params: {
      user_id: USER_ID,
    },
  });
  return response.data;
};

/**
 * Get habit patterns
 */
export const getHabitPatterns = async (
  days: number = 30
): Promise<{ habits: Pattern[]; count: number }> => {
  const response = await api.get('/patterns/habits', {
    params: {
      user_id: USER_ID,
      days,
    },
  });
  return response.data;
};

/**
 * Get anomalies
 */
export const getAnomalies = async (): Promise<{
  anomalies: Anomaly[];
  count: number;
}> => {
  const response = await api.get('/patterns/anomalies', {
    params: {
      user_id: USER_ID,
    },
  });
  return response.data;
};

/**
 * Get health summary
 */
export const getHealthSummary = async (
  days: number = 7
): Promise<any> => {
  const response = await api.get('/health/summary', {
    params: {
      user_id: USER_ID,
      days,
    },
  });
  return response.data;
};

/**
 * Health check
 */
export const healthCheck = async (): Promise<{
  status: string;
  timeline_connected: boolean;
  pattern_engine_ready: boolean;
}> => {
  const response = await api.get('/health');
  return response.data;
};

export default api;
