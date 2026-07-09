import { CssBaseline, ThemeProvider } from '@mui/material';
import { BrowserRouter, Navigate, Outlet, Route, Routes } from 'react-router-dom';
import { useSelector } from 'react-redux';
import DashboardLayout from './components/layout/DashboardLayout';
import DashboardPage from './pages/DashboardPage';
import InteractionsPage from './pages/InteractionsPage';
import LogInteractionPage from './pages/LogInteractionPage';
import LoginPage from './pages/LoginPage';
import DoctorDetailsPage from './pages/DoctorDetailsPage';
import theme from './theme';

function ProtectedLayout() {
  const user = useSelector((state) => state.auth.user);
  return user ? <DashboardLayout><Outlet /></DashboardLayout> : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route element={<ProtectedLayout />}>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/log" element={<LogInteractionPage />} />
            <Route path="/interactions" element={<InteractionsPage />} />
            <Route path="/doctors/:doctorId" element={<DoctorDetailsPage />} />
          </Route>
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}
