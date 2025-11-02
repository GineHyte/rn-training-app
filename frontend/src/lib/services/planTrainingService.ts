import api from '$lib/api';

export interface PlanTraining {
	id: number;
	name: string;
	startTime: string | null;
	endTime: string | null;
	intensity: number;
	planWeekId: number;
	createdAt: string;
	updatedAt: string;
}

export interface CreatePlanTrainingData {
	planWeekId: number;
	name: string;
	startTime: string | null;
	endTime: string | null;
	intensity: number;
}

export const planTrainingService = {
	async getByWeek(planWeekId: number): Promise<PlanTraining[]> {
		const response = await api.get<PlanTraining[]>(`/plan-trainings/week/${planWeekId}`);
		return response.data;
	},

	async getById(id: number): Promise<PlanTraining> {
		const response = await api.get<PlanTraining>(`/plan-trainings/${id}`);
		return response.data;
	},

	async create(data: CreatePlanTrainingData): Promise<PlanTraining> {
		const response = await api.post<PlanTraining>('/plan-trainings/', data);
		return response.data;
	},

	async delete(id: number): Promise<void> {
		await api.delete(`/plan-trainings/${id}`);
	}
};
