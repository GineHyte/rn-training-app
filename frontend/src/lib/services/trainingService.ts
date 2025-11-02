import api from '$lib/api';

export interface Training {
	id: number;
	startTime: string | null;
	endTime: string | null;
	planTrainingId: number;
	createdAt: string;
	updatedAt: string;
}

export interface CreateTrainingData {
	planTrainingId: number;
	startTime?: string | null;
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

export interface CreateTrainingExerciseData {
	trainingId: number;
	planExerciseId: number;
	reps: number;
	kgs: number;
	timestamp: string;
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

	async create(data: CreateTrainingData): Promise<Training> {
		const response = await api.post<Training>('/trainings/', data);
		return response.data;
	},

	async endTraining(id: number): Promise<Training> {
		const response = await api.post<Training>(`/trainings/${id}/end`);
		return response.data;
	},

	async delete(id: number): Promise<void> {
		await api.delete(`/trainings/${id}`);
	},

	// Training exercises
	async getExercises(trainingId: number): Promise<TrainingExercise[]> {
		const response = await api.get<TrainingExercise[]>(`/training-exercises/training/${trainingId}`);
		return response.data;
	},

	async addExercise(data: CreateTrainingExerciseData): Promise<TrainingExercise> {
		const response = await api.post<TrainingExercise>('/training-exercises/', data);
		return response.data;
	},

	async deleteExercise(id: number): Promise<void> {
		await api.delete(`/training-exercises/${id}`);
	}
};
