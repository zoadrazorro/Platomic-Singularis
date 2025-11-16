/**
 * Patterns Screen - View detected patterns and anomalies
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  ScrollView,
  RefreshControl,
  StyleSheet,
} from 'react-native';
import { Text, Card, Chip, ActivityIndicator, Button } from 'react-native-paper';
import { getAllPatterns, Pattern, Anomaly } from '../../services/api';

export default function PatternsScreen() {
  const [patterns, setPatterns] = useState<Pattern[]>([]);
  const [anomalies, setAnomalies] = useState<Anomaly[]>([]);
  const [alertLevel, setAlertLevel] = useState('NONE');
  const [isLoading, setIsLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const loadPatterns = async () => {
    try {
      setIsLoading(true);
      const data = await getAllPatterns();
      setPatterns(data.patterns || []);
      setAnomalies(data.anomalies || []);
      setAlertLevel(data.alert_level || 'NONE');
    } catch (error) {
      console.error('Failed to load patterns:', error);
    } finally {
      setIsLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    loadPatterns();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    loadPatterns();
  };

  const getAlertColor = (level: string) => {
    switch (level) {
      case 'CRITICAL':
        return '#e74c3c';
      case 'HIGH':
        return '#e67e22';
      case 'MEDIUM':
        return '#f39c12';
      default:
        return '#27ae60';
    }
  };

  if (isLoading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#4a90e2" />
        <Text style={styles.loadingText}>Analyzing patterns...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Patterns & Insights</Text>
        <Chip
          style={[styles.alertChip, { backgroundColor: getAlertColor(alertLevel) }]}
          textStyle={styles.alertText}
        >
          Alert Level: {alertLevel}
        </Chip>
      </View>

      <ScrollView
        style={styles.scrollView}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        {/* Anomalies */}
        {anomalies.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>⚠️ Anomalies</Text>
            {anomalies.map((anomaly, index) => (
              <Card key={index} style={[styles.card, styles.anomalyCard]}>
                <Card.Content>
                  <View style={styles.cardHeader}>
                    <Chip
                      style={[
                        styles.levelChip,
                        { backgroundColor: getAlertColor(anomaly.alert_level) },
                      ]}
                      textStyle={styles.levelText}
                    >
                      {anomaly.alert_level}
                    </Chip>
                  </View>
                  <Text style={styles.anomalyMessage}>{anomaly.message}</Text>
                  <Text style={styles.anomalyDetails}>
                    Expected: {anomaly.expected_value} • Actual: {anomaly.actual_value}
                  </Text>
                  <Text style={styles.anomalyDeviation}>
                    Deviation: {(anomaly.deviation * 100).toFixed(0)}%
                  </Text>
                </Card.Content>
                <Card.Actions>
                  <Button textColor="#fff">Dismiss</Button>
                  <Button textColor="#4a90e2">Details</Button>
                </Card.Actions>
              </Card>
            ))}
          </View>
        )}

        {/* Patterns */}
        {patterns.length > 0 ? (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>📊 Detected Patterns</Text>
            {patterns.map((pattern, index) => (
              <Card key={index} style={styles.card}>
                <Card.Content>
                  <View style={styles.cardHeader}>
                    <Text style={styles.patternName}>{pattern.name}</Text>
                    <Chip style={styles.confidenceChip} textStyle={styles.confidenceText}>
                      {(pattern.confidence * 100).toFixed(0)}%
                    </Chip>
                  </View>
                  <Text style={styles.patternDescription}>{pattern.description}</Text>
                  {pattern.evidence && pattern.evidence.length > 0 && (
                    <View style={styles.evidenceContainer}>
                      <Text style={styles.evidenceTitle}>Evidence:</Text>
                      {pattern.evidence.slice(0, 3).map((evidence, i) => (
                        <Text key={i} style={styles.evidenceItem}>
                          • {evidence}
                        </Text>
                      ))}
                    </View>
                  )}
                </Card.Content>
              </Card>
            ))}
          </View>
        ) : (
          <View style={styles.emptyContainer}>
            <Text style={styles.emptyText}>No patterns detected yet</Text>
            <Text style={styles.emptySubtext}>
              Keep logging your life and patterns will emerge over time
            </Text>
          </View>
        )}

        {/* Tips */}
        <View style={styles.section}>
          <Card style={[styles.card, styles.tipCard]}>
            <Card.Content>
              <Text style={styles.tipTitle}>💡 Pattern Detection Tips</Text>
              <Text style={styles.tipText}>
                • Patterns emerge after 7-14 days of consistent data{'\n'}
                • More data sources = better insights{'\n'}
                • Anomalies are detected in real-time{'\n'}
                • Critical alerts trigger notifications
              </Text>
            </Card.Content>
          </Card>
        </View>
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
  alertChip: {
    alignSelf: 'flex-start',
  },
  alertText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: 'bold',
  },
  scrollView: {
    flex: 1,
  },
  section: {
    padding: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 12,
  },
  card: {
    marginBottom: 12,
    backgroundColor: '#2c3e50',
  },
  anomalyCard: {
    borderLeftWidth: 4,
    borderLeftColor: '#e74c3c',
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  levelChip: {
    height: 24,
  },
  levelText: {
    color: '#fff',
    fontSize: 11,
    fontWeight: 'bold',
  },
  anomalyMessage: {
    fontSize: 16,
    color: '#fff',
    fontWeight: 'bold',
    marginBottom: 8,
  },
  anomalyDetails: {
    fontSize: 13,
    color: '#bbb',
    marginBottom: 4,
  },
  anomalyDeviation: {
    fontSize: 12,
    color: '#e74c3c',
    fontWeight: 'bold',
  },
  patternName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#fff',
    flex: 1,
  },
  confidenceChip: {
    backgroundColor: '#0f3460',
    height: 24,
  },
  confidenceText: {
    color: '#4a90e2',
    fontSize: 11,
    fontWeight: 'bold',
  },
  patternDescription: {
    fontSize: 14,
    color: '#ecf0f1',
    marginBottom: 8,
    lineHeight: 20,
  },
  evidenceContainer: {
    marginTop: 8,
    padding: 8,
    backgroundColor: '#1a1a2e',
    borderRadius: 8,
  },
  evidenceTitle: {
    fontSize: 12,
    color: '#aaa',
    marginBottom: 4,
    fontWeight: 'bold',
  },
  evidenceItem: {
    fontSize: 11,
    color: '#bbb',
    marginBottom: 2,
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
  tipCard: {
    backgroundColor: '#16213e',
    borderLeftWidth: 4,
    borderLeftColor: '#4a90e2',
  },
  tipTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#4a90e2',
    marginBottom: 8,
  },
  tipText: {
    fontSize: 13,
    color: '#bbb',
    lineHeight: 20,
  },
});
