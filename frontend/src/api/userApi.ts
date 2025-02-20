import api from './axios';
import { ProfileType } from '@/types/userTypes';

export async function retrieveProfile(): Promise<ProfileType> {
  const response = await api.get<ProfileType>(`/users`);
  return response.data;
}