import { useEffect } from 'react';
import { wsService } from '../services/websocket';

export const useWebSocket = (onAlertReceived: (alert: any) => void) => {
  useEffect(() => {
    wsService.connect();
    wsService.onAlert(onAlertReceived);

    return () => {
      wsService.disconnect();
    };
  }, [onAlertReceived]);
};