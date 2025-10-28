import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, Button, StyleSheet, TouchableOpacity, Alert } from 'react-native';
import { planService, Plan } from '../services/planService';

export default function PlansScreen({ navigation }: any) {
  const [plans, setPlans] = useState<Plan[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadPlans();
  }, []);

  const loadPlans = async () => {
    setLoading(true);
    try {
      const data = await planService.getAll();
      setPlans(data);
    } catch (error: any) {
      Alert.alert('Error', 'Failed to load plans');
    } finally {
      setLoading(false);
    }
  };

  const handleDeletePlan = async (id: number) => {
    Alert.alert('Delete Plan', 'Are you sure?', [
      { text: 'Cancel' },
      {
        text: 'Delete',
        onPress: async () => {
          try {
            await planService.delete(id);
            loadPlans();
          } catch (error) {
            Alert.alert('Error', 'Failed to delete plan');
          }
        },
      },
    ]);
  };

  const renderPlan = ({ item }: { item: Plan }) => (
    <TouchableOpacity
      style={styles.planItem}
      onPress={() => navigation.navigate('PlanDetail', { planId: item.id })}
    >
      <View>
        <Text style={styles.planName}>{item.name}</Text>
        <Text style={styles.planDate}>
          {new Date(item.startDate).toLocaleDateString()}
        </Text>
        <Text style={styles.planPublic}>{item.public ? 'Public' : 'Private'}</Text>
      </View>
      <Button title="Delete" onPress={() => handleDeletePlan(item.id)} color="red" />
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <Button title="Create New Plan" onPress={() => navigation.navigate('CreatePlan')} />
      {loading ? (
        <Text style={styles.loading}>Loading...</Text>
      ) : (
        <FlatList
          data={plans}
          renderItem={renderPlan}
          keyExtractor={(item) => item.id.toString()}
          refreshing={loading}
          onRefresh={loadPlans}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
  },
  loading: {
    textAlign: 'center',
    marginTop: 20,
  },
  planItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 15,
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 5,
    marginVertical: 5,
  },
  planName: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  planDate: {
    color: '#666',
  },
  planPublic: {
    color: '#999',
    fontSize: 12,
  },
});
