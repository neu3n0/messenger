export interface TestAppType {
  id: number;
  arg1: string;
  arg2: number;
  owner: string;
}

export interface UpdateTestAppType {
  arg1?: string;
  arg2?: number;
}

export interface createTestAppType {
  arg1: string;
  arg2: number;
}