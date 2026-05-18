import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import DashboardPage from './pages/DashboardPage';
import SensorsPage from './pages/SensorsPage';
import AlertsPage from './pages/AlertsPage';
import DevicesPage from './pages/DevicesPage';
import ThresholdsPage from './pages/ThresholdsPage';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/sensors" element={<SensorsPage />} />
          <Route path="/alerts" element={<AlertsPage />} />
          <Route path="/devices" element={<DevicesPage />} />
          <Route path="/settings" element={<ThresholdsPage />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;