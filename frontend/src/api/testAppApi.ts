// import { AxiosResponse } from 'axios';
import api from './axios';
import { TestAppType, UpdateTestAppType, createTestAppType } from '@/types/testAppTypes';

export async function fetchTestApps(): Promise<TestAppType[]> {
  const response = await api.get<TestAppType[]>('test_app/');
  return response.data;
}

export async function createTestApp(data: createTestAppType): Promise<TestAppType> {
// export async function createTestApp(data: { arg1: string; arg2: number }): Promise<TestAppType> {
  const response = await api.post<TestAppType>('test_app/', data);
  return response.data;
}

export async function updateTestApp(id: number, data: UpdateTestAppType): Promise<TestAppType> {
// export async function updateTestApp(id: number, data: Partial<{ arg1: string; arg2: number }>): Promise<TestAppType> {
  const response = await api.patch<TestAppType>(`test_app/${id}/`, data);
  return response.data;
}

// export const getListTestApp = async (): Promise<AxiosResponse<TestAppType[]>> => {
//   return api.get<TestAppType[]>('/test_app/');
// };

// export const updateTestApp = async (id: number, payload: UpdateTestAppType): Promise<TestAppType> => {
//   const response = await api.patch<TestAppType>(`/test_app/${id}/`, payload);
//   return response.data;
// };