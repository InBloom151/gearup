import { Routes, Route, Navigate } from 'react-router-dom';
import AuthPage from '../pages/AuthPage';
import DashboardPage from '../pages/DashboardPage';
import { useAuth } from '../contexts/AuthContext';

const AppRouter = () => {
  const { isAuthenticated } = useAuth();

  return (
    <Routes>
      <Route
        path="/auth"
        element={!isAuthenticated ? <AuthPage /> : <Navigate to="/dashboard" />}
      />
      <Route
        path="/dashboard"
        element={isAuthenticated ? <DashboardPage /> : <Navigate to="/auth" />}
      />
      <Route path="*" element={<Navigate to="/auth" />} />
    </Routes>
  );
};

export default AppRouter;