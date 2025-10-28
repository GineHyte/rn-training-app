import React, { useState } from 'react';
import { View, TextInput, Button, StyleSheet, Text, Alert, Switch, ScrollView } from 'react-native';
import { exerciseService } from '../services/exerciseService';

export default function CreateExerciseScreen({ navigation }: any) {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [video, setVideo] = useState('');
  const [image, setImage] = useState('');
  const [isPublic, setIsPublic] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleCreate = async () => {
    if (!name) {
      Alert.alert('Error', 'Please enter an exercise name');
      return;
    }

    setLoading(true);
    try {
      await exerciseService.create({
        name,
        description: description || undefined,
        video: video || undefined,
        image: image || undefined,
        public: isPublic,
      });
      Alert.alert('Success', 'Exercise created successfully', [
        { text: 'OK', onPress: () => navigation.goBack() }
      ]);
    } catch (error: any) {
      Alert.alert('Error', error.response?.data?.detail || 'Failed to create exercise');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>Create New Exercise</Text>
      <TextInput
        style={styles.input}
        placeholder="Exercise Name"
        value={name}
        onChangeText={setName}
      />
      <TextInput
        style={[styles.input, styles.textArea]}
        placeholder="Description"
        value={description}
        onChangeText={setDescription}
        multiline
        numberOfLines={4}
      />
      <TextInput
        style={styles.input}
        placeholder="Video URL (optional)"
        value={video}
        onChangeText={setVideo}
      />
      <TextInput
        style={styles.input}
        placeholder="Image URL (optional)"
        value={image}
        onChangeText={setImage}
      />
      <View style={styles.switchContainer}>
        <Text>Public Exercise</Text>
        <Switch value={isPublic} onValueChange={setIsPublic} />
      </View>
      <Button title={loading ? 'Creating...' : 'Create Exercise'} onPress={handleCreate} disabled={loading} />
    </ScrollView>
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
  textArea: {
    height: 100,
    textAlignVertical: 'top',
  },
  switchContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
});
