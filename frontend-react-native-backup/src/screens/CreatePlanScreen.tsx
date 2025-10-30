import React, { useState } from 'react';
import { View, TextInput, Button, StyleSheet, Text, Alert, Switch } from 'react-native';
import { planService } from '../services/planService';

export default function CreatePlanScreen({ navigation }: any) {
  const [name, setName] = useState('');
  const [startDate, setStartDate] = useState(new Date().toISOString().split('T')[0]);
  const [isPublic, setIsPublic] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleCreate = async () => {
    if (!name) {
      Alert.alert('Error', 'Please enter a plan name');
      return;
    }

    setLoading(true);
    try {
      await planService.create({
        name,
        startDate: new Date(startDate).toISOString(),
        public: isPublic,
      });
      Alert.alert('Success', 'Plan created successfully', [
        { text: 'OK', onPress: () => navigation.goBack() }
      ]);
    } catch (error: any) {
      Alert.alert('Error', error.response?.data?.detail || 'Failed to create plan');
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Create New Plan</Text>
      <TextInput
        style={styles.input}
        placeholder="Plan Name"
        value={name}
        onChangeText={setName}
      />
      <TextInput
        style={styles.input}
        placeholder="Start Date (YYYY-MM-DD)"
        value={startDate}
        onChangeText={setStartDate}
      />
      <View style={styles.switchContainer}>
        <Text>Public Plan</Text>
        <Switch value={isPublic} onValueChange={setIsPublic} />
      </View>
      <Button title={loading ? 'Creating...' : 'Create Plan'} onPress={handleCreate} disabled={loading} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 5,
    padding: 10,
    marginBottom: 15,
  },
  switchContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
});
