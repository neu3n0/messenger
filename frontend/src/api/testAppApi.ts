import { AxiosResponse } from 'axios';
import api from './axios';
import { TestAppType, UpdateTestAppType } from '../types/testAppTypes';

export const getListTestApp = async (): Promise<AxiosResponse<TestAppType[]>> => {
  return api.get<TestAppType[]>('/test_app/');
};

export const updateTestApp = async (id: number, payload: UpdateTestAppType): Promise<TestAppType> => {
  const response = await api.patch<TestAppType>(`/test_app/${id}/`, payload);
  return response.data;
};
