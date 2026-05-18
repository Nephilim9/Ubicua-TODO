import DeviceCard from './DeviceCard';

const devicesData = [
  { name: 'Nodo Maestro', mac: 'A4:CF:12:34:56:78', type: 'MASTER', status: 'online' as const, lastSeen: 'Justo ahora' },
  { name: 'Sensor Sala', mac: 'B4:CF:12:34:56:79', type: 'SLAVE', status: 'online' as const, lastSeen: 'Hace 2 min' },
  { name: 'Sensor Garage', mac: 'C4:CF:12:34:56:80', type: 'SLAVE', status: 'offline' as const, lastSeen: 'Hace 1 día' },
];

const DeviceList = () => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {devicesData.map((dev) => (
        <DeviceCard key={dev.mac} device={dev} />
      ))}
    </div>
  );
};

export default DeviceList;