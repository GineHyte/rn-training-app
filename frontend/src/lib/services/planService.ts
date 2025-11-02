import api from '$lib/api';

export interface Plan {
	id: number;
	name: string;
	startDate: string | null;
	public: boolean;
	userId: number;
	createdAt: string;
	updatedAt: string;
}

export interface CreatePlanData {
	name: string;
	startDate?: string | null;
	public: boolean;
}

export interface UpdatePlanData {
	name?: string;
	startDate?: string | null;
	public?: boolean;
}

export const planService = {
	async getAll(): Promise<Plan[]> {
		const response = await api.get<Plan[]>('/plans/');
		return response.data;
	},

	async getById(id: number): Promise<Plan> {
		const response = await api.get<Plan>(`/plans/${id}`);
		return response.data;
	},

	async create(data: CreatePlanData): Promise<Plan> {
		const response = await api.post<Plan>('/plans/', data);
		return response.data;
	},

	async update(id: number, data: UpdatePlanData): Promise<Plan> {
		const response = await api.put<Plan>(`/plans/${id}`, data);
		return response.data;
	},

	async delete(id: number): Promise<void> {
		await api.delete(`/plans/${id}`);
	}
};
