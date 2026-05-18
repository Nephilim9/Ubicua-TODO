import { create } from 'zustand';
import { Device } from '../types/device';

interface DeviceState {
  devices: Device[];
  setDevices: (devices: Device[]) => void;
  updateDeviceStatus: (mac: string, status: 'online' | 'offline') => void;
}

export const useDeviceStore = create<DeviceState>((set) => ({
  devices: [],
  setDevices: (devices) => set({ devices }),
  updateDeviceStatus: (mac, status) => set((state) => ({
    devices: state.devices.map(d => 
      d.mac_address === mac ? { ...d, status } : d
    )
  })),
}));