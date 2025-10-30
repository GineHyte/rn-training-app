import api from './api';
import AsyncStorage from '@react-native-async-storage/async-storage';

export interface LoginData {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export const authService = {
  async login(data: LoginData): Promise<TokenResponse> {
    const response = await api.post<TokenResponse>('/auth/login', data);
    await AsyncStorage.setItem('token', response.data.access_token);
    return response.data;
  },

  async register(data: RegisterData) {
    const response = await api.post('/auth/register', data);
    return response.data;
  },

  async logout() {
    await AsyncStorage.removeItem('token');
  },

  async getToken() {
    return await AsyncStorage.getItem('token');
  },
};
