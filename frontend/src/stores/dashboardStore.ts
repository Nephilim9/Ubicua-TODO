import { create } from 'zustand';

interface DashboardState {
  isLiveMode: boolean;
  toggleLiveMode: () => void;
  lastRefresh: string | null;
  setLastRefresh: (time: string) => void;
}

export const useDashboardStore = create<DashboardState>((set) => ({
  isLiveMode: true,
  toggleLiveMode: () => set((state) => ({ isLiveMode: !state.isLiveMode })),
  lastRefresh: null,
  setLastRefresh: (time) => set({ lastRefresh: time }),
}));