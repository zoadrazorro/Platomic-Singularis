/**
 * Chat Screen - Main interface for talking with Sophia
 */

import React, { useState, useRef, useEffect } from 'react';
import {
  View,
  ScrollView,
  TextInput,
  TouchableOpacity,
  KeyboardAvoidingView,
  Platform,
  StyleSheet,
} from 'react-native';
import { Text, IconButton, Chip } from 'react-native-paper';
import { useChatStore } from '../../stores/chatStore';
import * as Speech from 'expo-speech';

const QUICK_ACTIONS = [
  { label: '💤 Sleep', query: 'How did I sleep last night?' },
  { label: '🏃 Exercise', query: 'Am I exercising enough?' },
  { label: '📊 Patterns', query: 'What patterns do you see this week?' },
  { label: '🏠 Home', query: 'How much time did I spend at home?' },
];

export default function ChatScreen() {
  const { messages, isLoading, sendMessage } = useChatStore();
  const [inputText, setInputText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const scrollViewRef = useRef<ScrollView>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    scrollViewRef.current?.scrollToEnd({ animated: true });
  }, [messages]);

  const handleSend = async () => {
    if (inputText.trim()) {
      await sendMessage(inputText.trim());
      setInputText('');
    }
  };

  const handleQuickAction = async (query: string) => {
    await sendMessage(query);
  };

  const handleVoiceInput = async () => {
    // TODO: Implement voice recognition with expo-speech
    // For now, show placeholder
    setIsRecording(true);
    setTimeout(() => {
      setIsRecording(false);
      // Would set inputText with transcribed speech
    }, 2000);
  };

  const speakMessage = (text: string) => {
    Speech.speak(text, {
      language: 'en-US',
      pitch: 1.0,
      rate: 0.9,
    });
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      keyboardVerticalOffset={100}
    >
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Sophia 🦉</Text>
        <Text style={styles.headerSubtitle}>Life Examination Assistant</Text>
      </View>

      {/* Messages */}
      <ScrollView
        ref={scrollViewRef}
        style={styles.messagesContainer}
        contentContainerStyle={styles.messagesContent}
      >
        {messages.map((message, index) => (
          <View
            key={index}
            style={[
              styles.messageBubble,
              message.role === 'user' ? styles.userBubble : styles.assistantBubble,
            ]}
          >
            <Text
              style={[
                styles.messageText,
                message.role === 'user' ? styles.userText : styles.assistantText,
              ]}
            >
              {message.content}
            </Text>
            <Text style={styles.messageTime}>
              {message.timestamp.toLocaleTimeString([], {
                hour: '2-digit',
                minute: '2-digit',
              })}
            </Text>
            {message.role === 'assistant' && (
              <IconButton
                icon="volume-high"
                size={16}
                onPress={() => speakMessage(message.content)}
                style={styles.speakButton}
              />
            )}
          </View>
        ))}
        {isLoading && (
          <View style={[styles.messageBubble, styles.assistantBubble]}>
            <Text style={styles.assistantText}>Sophia is thinking...</Text>
          </View>
        )}
      </ScrollView>

      {/* Quick Actions */}
      <ScrollView
        horizontal
        style={styles.quickActions}
        showsHorizontalScrollIndicator={false}
      >
        {QUICK_ACTIONS.map((action, index) => (
          <Chip
            key={index}
            onPress={() => handleQuickAction(action.query)}
            style={styles.quickActionChip}
            textStyle={styles.quickActionText}
          >
            {action.label}
          </Chip>
        ))}
      </ScrollView>

      {/* Input */}
      <View style={styles.inputContainer}>
        <IconButton
          icon={isRecording ? 'microphone' : 'microphone-outline'}
          size={24}
          onPress={handleVoiceInput}
          iconColor={isRecording ? '#e74c3c' : '#4a90e2'}
        />
        <TextInput
          style={styles.input}
          value={inputText}
          onChangeText={setInputText}
          placeholder="Ask Sophia anything..."
          placeholderTextColor="#999"
          multiline
          maxLength={500}
          onSubmitEditing={handleSend}
        />
        <IconButton
          icon="send"
          size={24}
          onPress={handleSend}
          disabled={!inputText.trim() || isLoading}
          iconColor={inputText.trim() ? '#4a90e2' : '#ccc'}
        />
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1a2e',
  },
  header: {
    padding: 16,
    paddingTop: 60,
    backgroundColor: '#16213e',
    borderBottomWidth: 1,
    borderBottomColor: '#0f3460',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#aaa',
    marginTop: 4,
  },
  messagesContainer: {
    flex: 1,
  },
  messagesContent: {
    padding: 16,
  },
  messageBubble: {
    maxWidth: '80%',
    padding: 12,
    borderRadius: 16,
    marginBottom: 12,
  },
  userBubble: {
    alignSelf: 'flex-end',
    backgroundColor: '#4a90e2',
  },
  assistantBubble: {
    alignSelf: 'flex-start',
    backgroundColor: '#2c3e50',
  },
  messageText: {
    fontSize: 16,
    lineHeight: 22,
  },
  userText: {
    color: '#fff',
  },
  assistantText: {
    color: '#ecf0f1',
  },
  messageTime: {
    fontSize: 11,
    color: '#bbb',
    marginTop: 4,
  },
  speakButton: {
    position: 'absolute',
    right: 4,
    bottom: 4,
  },
  quickActions: {
    maxHeight: 50,
    paddingHorizontal: 16,
    paddingVertical: 8,
    backgroundColor: '#16213e',
  },
  quickActionChip: {
    marginRight: 8,
    backgroundColor: '#0f3460',
  },
  quickActionText: {
    color: '#fff',
    fontSize: 12,
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 8,
    backgroundColor: '#16213e',
    borderTopWidth: 1,
    borderTopColor: '#0f3460',
  },
  input: {
    flex: 1,
    backgroundColor: '#2c3e50',
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 8,
    color: '#fff',
    fontSize: 16,
    maxHeight: 100,
  },
});
