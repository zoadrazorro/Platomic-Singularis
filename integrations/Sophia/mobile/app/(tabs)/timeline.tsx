/**
 * Timeline Screen - View all life events
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  ScrollView,
  RefreshControl,
  StyleSheet,
} from 'react-native';
import { Text, Card, Chip, ActivityIndicator } from 'react-native-paper';
import { getTimelineEvents, LifeEvent } from '../../services/api';
import { format, parseISO } from 'date-fns';

const EVENT_ICONS: Record<string, string> = {
  sleep: '💤',
  exercise: '🏃',
  heart_rate: '❤️',
  steps: '👣',
  meal: '🍽️',
  work_session: '💼',
  break: '☕',
  arrive_home: '🏠',
  leave_home: '🚪',
  room_enter: '🚶',
  message: '💬',
  fall: '⚠️',
  anomaly: '🚨',
  other: '📝',
};

export default function TimelineScreen() {
  const [events, setEvents] = useState<LifeEvent[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [days, setDays] = useState(7);

  const loadEvents = async () => {
    try {
      setIsLoading(true);
      const data = await getTimelineEvents(days);
      setEvents(data.events);
    } catch (error) {
      console.error('Failed to load events:', error);
    } finally {
      setIsLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    loadEvents();
  }, [days]);

  const onRefresh = () => {
    setRefreshing(true);
    loadEvents();
  };

  const groupEventsByDay = (events: LifeEvent[]) => {
    const grouped: Record<string, LifeEvent[]> = {};
    events.forEach(event => {
      const day = format(parseISO(event.timestamp), 'yyyy-MM-dd');
      if (!grouped[day]) {
        grouped[day] = [];
      }
      grouped[day].push(event);
    });
    return grouped;
  };

  const groupedEvents = groupEventsByDay(events);
  const sortedDays = Object.keys(groupedEvents).sort().reverse();

  if (isLoading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#4a90e2" />
        <Text style={styles.loadingText}>Loading timeline...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Timeline</Text>
        <View style={styles.filterRow}>
          {[7, 14, 30].map(d => (
            <Chip
              key={d}
              selected={days === d}
              onPress={() => setDays(d)}
              style={styles.filterChip}
              textStyle={styles.filterText}
            >
              {d} days
            </Chip>
          ))}
        </View>
      </View>

      {/* Events */}
      <ScrollView
        style={styles.scrollView}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        {sortedDays.length === 0 ? (
          <View style={styles.emptyContainer}>
            <Text style={styles.emptyText}>No events yet</Text>
            <Text style={styles.emptySubtext}>
              Start logging your life and events will appear here
            </Text>
          </View>
        ) : (
          sortedDays.map(day => (
            <View key={day} style={styles.dayGroup}>
              <Text style={styles.dayHeader}>
                {format(parseISO(day), 'EEEE, MMMM d')}
              </Text>
              {groupedEvents[day].map(event => (
                <Card key={event.id} style={styles.eventCard}>
                  <Card.Content style={styles.eventContent}>
                    <Text style={styles.eventIcon}>
                      {EVENT_ICONS[event.type] || EVENT_ICONS.other}
                    </Text>
                    <View style={styles.eventDetails}>
                      <Text style={styles.eventType}>
                        {event.type.replace(/_/g, ' ').toUpperCase()}
                      </Text>
                      <Text style={styles.eventTime}>
                        {format(parseISO(event.timestamp), 'h:mm a')}
                      </Text>
                      {Object.keys(event.features).length > 0 && (
                        <Text style={styles.eventFeatures}>
                          {Object.entries(event.features)
                            .slice(0, 2)
                            .map(([key, value]) => `${key}: ${value}`)
                            .join(' • ')}
                        </Text>
                      )}
                    </View>
                    <Chip style={styles.sourceChip} textStyle={styles.sourceText}>
                      {event.source}
                    </Chip>
                  </Card.Content>
                </Card>
              ))}
            </View>
          ))
        )}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1a2e',
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#1a1a2e',
  },
  loadingText: {
    color: '#fff',
    marginTop: 16,
    fontSize: 16,
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
    marginBottom: 12,
  },
  filterRow: {
    flexDirection: 'row',
    gap: 8,
  },
  filterChip: {
    backgroundColor: '#0f3460',
  },
  filterText: {
    color: '#fff',
    fontSize: 12,
  },
  scrollView: {
    flex: 1,
  },
  emptyContainer: {
    padding: 32,
    alignItems: 'center',
  },
  emptyText: {
    fontSize: 18,
    color: '#fff',
    marginBottom: 8,
  },
  emptySubtext: {
    fontSize: 14,
    color: '#aaa',
    textAlign: 'center',
  },
  dayGroup: {
    marginBottom: 24,
  },
  dayHeader: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#4a90e2',
    padding: 16,
    paddingBottom: 8,
  },
  eventCard: {
    marginHorizontal: 16,
    marginBottom: 8,
    backgroundColor: '#2c3e50',
  },
  eventContent: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  eventIcon: {
    fontSize: 32,
  },
  eventDetails: {
    flex: 1,
  },
  eventType: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 4,
  },
  eventTime: {
    fontSize: 12,
    color: '#aaa',
    marginBottom: 4,
  },
  eventFeatures: {
    fontSize: 11,
    color: '#bbb',
  },
  sourceChip: {
    backgroundColor: '#0f3460',
    height: 24,
  },
  sourceText: {
    fontSize: 10,
    color: '#fff',
  },
});
