import { create } from 'zustand';
import { Alert } from '../types/alert';

interface AlertState {
  activeAlerts: Alert[];
  unreadCount: number;
  addAlert: (alert: Alert) => void;
  clearAlerts: () => void;
  markAsRead: () => void;
}

export const useAlertStore = create<AlertState>((set) => ({
  activeAlerts: [],
  unreadCount: 0,
  addAlert: (alert) => set((state) => ({
    activeAlerts: [alert, ...state.activeAlerts],
    unreadCount: state.unreadCount + 1
  })),
  clearAlerts: () => set({ activeAlerts: [], unreadCount: 0 }),
  markAsRead: () => set({ unreadCount: 0 }),
}));