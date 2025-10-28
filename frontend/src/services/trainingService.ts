import api from './api';

export interface Training {
  id: number;
  startTime: string;
  endTime?: string;
  planTrainingId: number;
  createdAt: string;
  updatedAt: string;
}

export interface TrainingCreate {
  planTrainingId: number;
  startTime: string;
}

export interface TrainingExercise {
  id: number;
  reps: number;
  kgs: number;
  timestamp: string;
  trainingId: number;
  planExerciseId: number;
  createdAt: string;
  updatedAt: string;
}

export interface TrainingExerciseCreate {
  reps: number;
  kgs: number;
  timestamp: string;
  trainingId: number;
  planExerciseId: number;
}

export const trainingService = {
  async getAll(): Promise<Training[]> {
    const response = await api.get<Training[]>('/trainings/');
    return response.data;
  },

  async getById(id: number): Promise<Training> {
    const response = await api.get<Training>(`/trainings/${id}`);
    return response.data;
  },

  async create(data: TrainingCreate): Promise<Training> {
    const response = await api.post<Training>('/trainings/', data);
    return response.data;
  },

  async end(id: number): Promise<Training> {
    const response = await api.post<Training>(`/trainings/${id}/end`);
    return response.data;
  },

  async delete(id: number): Promise<void> {
    await api.delete(`/trainings/${id}`);
  },

  // Training Exercises
  async getTrainingExercises(trainingId: number): Promise<TrainingExercise[]> {
    const response = await api.get<TrainingExercise[]>(`/training-exercises/training/${trainingId}`);
    return response.data;
  },

  async createTrainingExercise(data: TrainingExerciseCreate): Promise<TrainingExercise> {
    const response = await api.post<TrainingExercise>('/training-exercises/', data);
    return response.data;
  },

  async deleteTrainingExercise(id: number): Promise<void> {
    await api.delete(`/training-exercises/${id}`);
  },
};
