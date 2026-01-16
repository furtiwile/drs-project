import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './application/context/AuthContext';
import { ProtectedRoute } from './application/components/ProtectedRoute';
import { Login } from './presentation/pages/Auth/Login';
import { Register } from './presentation/pages/Auth/Register';
import { Home } from './presentation/pages/Home/Home';
import { Account } from './presentation/pages/Account/Account';
import { UserManagement } from './presentation/pages/UserManagement/UserManagement';
import { MainLayout } from './presentation/layouts/MainLayout/MainLayout';
import './App.css';

function App() {
  return (
    <AuthProvider>
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
          
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
