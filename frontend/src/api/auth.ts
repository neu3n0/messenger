import api from './axios';

export interface LoginData {
  username: string;
  password: string;
}

export async function login(data: LoginData): Promise<void> {
  await api.post('token/', data);
}

export async function logoutUser(): Promise<void> {
  await api.post('logout/');
}