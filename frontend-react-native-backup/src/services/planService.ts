import api from './api';

export interface Plan {
  id: number;
  name: string;
  startDate: string;
  public: boolean;
  userId: number;
  createdAt: string;
  updatedAt: string;
}

export interface PlanCreate {
  name: string;
  startDate: string;
  public: boolean;
}

export interface PlanUpdate {
  name?: string;
  startDate?: string;
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

  async create(data: PlanCreate): Promise<Plan> {
    const response = await api.post<Plan>('/plans/', data);
    return response.data;
  },

  async update(id: number, data: PlanUpdate): Promise<Plan> {
    const response = await api.put<Plan>(`/plans/${id}`, data);
    return response.data;
  },

  async delete(id: number): Promise<void> {
    await api.delete(`/plans/${id}`);
  },
};
