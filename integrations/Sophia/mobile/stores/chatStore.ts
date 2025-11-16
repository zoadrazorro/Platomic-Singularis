/**
 * Chat Store
 * 
 * Manages conversation state with Sophia
 */

import { create } from 'zustand';
import { chatWithSophia, ChatMessage, ChatResponse } from '../services/api';

interface ChatStore {
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  
  sendMessage: (content: string) => Promise<void>;
  clearMessages: () => void;
  addMessage: (message: ChatMessage) => void;
}

export const useChatStore = create<ChatStore>((set, get) => ({
  messages: [
    {
      role: 'assistant',
      content: 'Hello! I\'m Sophia. Ask me anything about your life - sleep, exercise, patterns, or daily routines.',
      timestamp: new Date(),
    },
  ],
  isLoading: false,
  error: null,

  sendMessage: async (content: string) => {
    const { messages } = get();
    
    // Add user message
    const userMessage: ChatMessage = {
      role: 'user',
      content,
      timestamp: new Date(),
    };
    
    set({ messages: [...messages, userMessage], isLoading: true, error: null });

    try {
      // Send to API
      const response = await chatWithSophia(content, messages);
      
      // Add assistant response
      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: response.answer,
        timestamp: new Date(),
      };
      
      set(state => ({
        messages: [...state.messages, assistantMessage],
        isLoading: false,
      }));
    } catch (error) {
      console.error('Chat error:', error);
      set({
        error: 'Failed to get response from Sophia. Check your connection.',
        isLoading: false,
      });
    }
  },

  clearMessages: () => {
    set({
      messages: [
        {
          role: 'assistant',
          content: 'Conversation cleared. How can I help you?',
          timestamp: new Date(),
        },
      ],
    });
  },

  addMessage: (message: ChatMessage) => {
    set(state => ({
      messages: [...state.messages, message],
    }));
  },
}));
