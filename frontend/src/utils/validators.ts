export const isValidMacAddress = (mac: string): boolean => {
  const macRegex = /^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$/;
  return macRegex.test(mac);
};

export const isValidThresholdValue = (value: number, type: string): boolean => {
  if (type === 'HUMIDITY' && (value < 0 || value > 100)) return false;
  if (type === 'MQ135' && value < 0) return false;
  return true;
};