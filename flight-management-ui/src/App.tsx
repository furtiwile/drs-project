import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './application/context/AuthContext';
import { ToastProvider } from './application/context/ToastContext';
import { SocketProvider } from './application/context/SocketContext';
import { ProtectedRoute } from './application/components/ProtectedRoute';
import { Login } from './presentation/pages/Auth/Login';
import { Register } from './presentation/pages/Auth/Register';
import { Home } from './presentation/pages/Home/Home';
import { Account } from './presentation/pages/Account/Account';
import { UserManagement } from './presentation/pages/UserManagement/UserManagement';
import { AdminDashboard } from './presentation/pages/Admin/AdminDashboard';
import { ManagerDashboard } from './presentation/pages/Manager/ManagerDashboard';
import { FlightsPage } from './presentation/pages/Flights/FlightsPage';
import { MyBookingsPage } from './presentation/pages/Bookings/MyBookingsPage';
import { Reports } from './presentation/pages/Reports/Reports';
import { MainLayout } from './presentation/layouts/MainLayout/MainLayout';
import { Role } from './domain/enums/Role';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <ToastProvider>
        <SocketProvider>
          <BrowserRouter>
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              
              <Route
                path="/"
                element={
                  <ProtectedRoute>
                    <MainLayout>
                      <Home />
                    </MainLayout>
                  </ProtectedRoute>
                }
              />
              
              <Route
                path="/account"
                element={
                  <ProtectedRoute>
                    <MainLayout>
                      <Account />
                    </MainLayout>
                  </ProtectedRoute>
                }
              />
              
              <Route
                path="/users"
                element={
                  <ProtectedRoute>
                    <MainLayout>
                      <UserManagement />
                    </MainLayout>
                  </ProtectedRoute>
                }
              />
              
              <Route
                path="/admin/dashboard"
                element={
                  <ProtectedRoute requiredRole={Role.ADMINISTRATOR}>
                    <MainLayout>
                      <AdminDashboard />
                    </MainLayout>
                  </ProtectedRoute>
                }
              />

              <Route
                path="/admin/reports"
                element={
                  <ProtectedRoute requiredRole={Role.ADMINISTRATOR}>
                    <MainLayout>
                      <Reports />
                    </MainLayout>
                  </ProtectedRoute>
                }
              />
              
              <Route
                path="/manager/dashboard"
                element={
                  <ProtectedRoute requiredRole={Role.MANAGER}>
                    <MainLayout>
                      <ManagerDashboard />
                    </MainLayout>
                  </ProtectedRoute>
                }
              />
              
              <Route
                path="/flights"
                element={
                  <ProtectedRoute>
                    <MainLayout>
                      <FlightsPage />
                    </MainLayout>
                  </ProtectedRoute>
                }
              />
              
              <Route
                path="/bookings"
                element={
                  <ProtectedRoute>
                    <MainLayout>
                      <MyBookingsPage />
                    </MainLayout>
                  </ProtectedRoute>
                }
              />
              
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </BrowserRouter>
        </SocketProvider>
      </ToastProvider>
    </AuthProvider>
  );
}

export default App;
