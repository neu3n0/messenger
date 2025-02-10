import { create } from 'zustand';

interface AuthState {
  isAuthenticated: boolean;
  user: string | null;
  setAuth: (auth: boolean, user?: string | null) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  isAuthenticated: false,
  user: null,
  setAuth: (auth, user = null) => set({ isAuthenticated: auth, user }),
  logout: () => set({ isAuthenticated: false, user: null }),
}));