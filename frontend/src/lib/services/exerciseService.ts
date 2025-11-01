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
	async getAll(search?: string, filterType?: 'my' | 'public'): Promise<Exercise[]> {
		const params = new URLSearchParams();
		if (search) params.append('search', search);
		if (filterType) params.append('filter_type', filterType);
		
		const url = `/exercises/${params.toString() ? '?' + params.toString() : ''}`;
		const response = await api.get<Exercise[]>(url);
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
