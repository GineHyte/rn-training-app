import api from '$lib/api';

export interface PlanExercise {
	id: number;
	intensity: number;
	planTrainingId: number;
	exerciseId: number;
	exercise: {
		id: number;
		name: string;
		description?: string;
		video?: string;
		image?: string;
	};
	createdAt: string;
	updatedAt: string;
}

export interface CreatePlanExerciseData {
	planTrainingId: number;
	exerciseId: number;
	intensity: number;
}

export const planExerciseService = {
	async getByTraining(planTrainingId: number): Promise<PlanExercise[]> {
		const response = await api.get<PlanExercise[]>(`/plan-exercises/training/${planTrainingId}`);
		return response.data;
	},

	async create(data: CreatePlanExerciseData): Promise<PlanExercise> {
		const response = await api.post<PlanExercise>('/plan-exercises/', data);
		return response.data;
	},

	async delete(id: number): Promise<void> {
		await api.delete(`/plan-exercises/${id}`);
	}
};
