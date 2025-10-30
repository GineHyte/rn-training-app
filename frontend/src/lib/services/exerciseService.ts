import api from '$lib/api';

export interface Exercise {
	id: number;
	name: string;
	description?: string;
	video?: string;
	image?: string;
	public: boolean;
	userId: number;
	createdAt: string;
	updatedAt: string;
}

export interface CreateExerciseData {
	name: string;
	description?: string;
	video?: string;
	image?: string;
	public: boolean;
}

export interface UpdateExerciseData {
	name?: string;
	description?: string;
	video?: string;
	image?: string;
	public?: boolean;
}

export const exerciseService = {
	async getAll(): Promise<Exercise[]> {
		const response = await api.get<Exercise[]>('/exercises/');
		return response.data;
	},

	async getById(id: number): Promise<Exercise> {
		const response = await api.get<Exercise>(`/exercises/${id}`);
		return response.data;
	},

	async create(data: CreateExerciseData): Promise<Exercise> {
		const response = await api.post<Exercise>('/exercises/', data);
		return response.data;
	},

	async update(id: number, data: UpdateExerciseData): Promise<Exercise> {
		const response = await api.put<Exercise>(`/exercises/${id}`, data);
		return response.data;
	},

	async delete(id: number): Promise<void> {
		await api.delete(`/exercises/${id}`);
	}
};
