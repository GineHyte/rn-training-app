import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, Button, StyleSheet, TouchableOpacity, Alert } from 'react-native';
import { exerciseService, Exercise } from '../services/exerciseService';

export default function ExercisesScreen({ navigation }: any) {
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadExercises();
  }, []);

  const loadExercises = async () => {
    setLoading(true);
    try {
      const data = await exerciseService.getAll();
      setExercises(data);
    } catch (error: any) {
      Alert.alert('Error', 'Failed to load exercises');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteExercise = async (id: number) => {
    Alert.alert('Delete Exercise', 'Are you sure?', [
      { text: 'Cancel' },
      {
        text: 'Delete',
        onPress: async () => {
          try {
            await exerciseService.delete(id);
            loadExercises();
          } catch (error) {
            Alert.alert('Error', 'Failed to delete exercise');
          }
        },
      },
    ]);
  };

  const renderExercise = ({ item }: { item: Exercise }) => (
    <TouchableOpacity
      style={styles.exerciseItem}
      onPress={() => navigation.navigate('ExerciseDetail', { exerciseId: item.id })}
    >
      <View style={styles.exerciseInfo}>
        <Text style={styles.exerciseName}>{item.name}</Text>
        {item.description && (
          <Text style={styles.exerciseDesc} numberOfLines={2}>
            {item.description}
          </Text>
        )}
        <Text style={styles.exercisePublic}>{item.public ? 'Public' : 'Private'}</Text>
      </View>
      <Button title="Delete" onPress={() => handleDeleteExercise(item.id)} color="red" />
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <Button title="Create New Exercise" onPress={() => navigation.navigate('CreateExercise')} />
      {loading ? (
        <Text style={styles.loading}>Loading...</Text>
      ) : (
        <FlatList
          data={exercises}
          renderItem={renderExercise}
          keyExtractor={(item) => item.id.toString()}
          refreshing={loading}
          onRefresh={loadExercises}
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
  exerciseItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 15,
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 5,
    marginVertical: 5,
  },
  exerciseInfo: {
    flex: 1,
    marginRight: 10,
  },
  exerciseName: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  exerciseDesc: {
    color: '#666',
    marginTop: 5,
  },
  exercisePublic: {
    color: '#999',
    fontSize: 12,
    marginTop: 5,
  },
});
