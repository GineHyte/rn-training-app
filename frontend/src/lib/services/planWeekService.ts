import api from '$lib/api';

export interface PlanWeek {
	id: number;
	startDate: string;
	planId: number;
	createdAt: string;
	updatedAt: string;
}

export interface CreatePlanWeekData {
	planId: number;
	startDate: string;
}

export const planWeekService = {
	async getByPlan(planId: number): Promise<PlanWeek[]> {
		const response = await api.get<PlanWeek[]>(`/plan-weeks/plan/${planId}`);
		return response.data;
	},

	async create(data: CreatePlanWeekData): Promise<PlanWeek> {
		const response = await api.post<PlanWeek>('/plan-weeks/', data);
		return response.data;
	},

	async delete(id: number): Promise<void> {
		await api.delete(`/plan-weeks/${id}`);
	}
};
