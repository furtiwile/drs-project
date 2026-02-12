import { useState } from 'react';
import { useAuth } from '../../../application/context/AuthContext';
import { Role } from '../../../domain/enums/Role';
import { BalanceDialog } from './BalanceDialog';
import './Home.css';

export const Home = () => {
  const { user, refreshUser } = useAuth();
  const [isBalanceDialogOpen, setIsBalanceDialogOpen] = useState(false);

  const handleTransactionComplete = async () => {
    await refreshUser();
  };

  return (
    <div className="home-container">
      <div className="welcome-section">
        <h1>Welcome back, {user?.first_name}!</h1>
        <p>Your flight management dashboard</p>
      </div>

      <div className="dashboard-grid">
        <div className="dashboard-card">
          <div className="card-icon" style={{ background: 'rgba(139, 92, 246, 0.1)' }}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#8b5cf6" strokeWidth="2">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
              <polyline points="3.27 6.96 12 12.01 20.73 6.96" />
              <line x1="12" y1="22.08" x2="12" y2="12" />
            </svg>
          </div>
          <div className="card-content">
            <h3>Your Role</h3>
            <p className="card-value">{user?.role}</p>
            <p className="card-description">
              {user?.role === Role.ADMINISTRATOR && 'Full system access'}
              {user?.role === Role.MANAGER && 'Can manage flights and airlines'}
              {user?.role === Role.USER && 'Standard user access'}
            </p>
          </div>
        </div>

        <div className="dashboard-card balance-card" onClick={() => setIsBalanceDialogOpen(true)}>
          <div className="card-icon" style={{ background: 'rgba(34, 197, 94, 0.1)' }}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#22c55e" strokeWidth="2">
              <line x1="12" y1="1" x2="12" y2="23" />
              <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
            </svg>
          </div>
          <div className="card-content">
            <h3>Account Balance</h3>
            <p className="card-value">${user?.account_balance.toFixed(2)}</p>
            <p className="card-description">Available for bookings</p>
          </div>
        </div>

        <div className="dashboard-card">
          <div className="card-icon" style={{ background: 'rgba(59, 130, 246, 0.1)' }}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" strokeWidth="2">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
              <circle cx="9" cy="7" r="4" />
              <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
              <path d="M16 3.13a4 4 0 0 1 0 7.75" />
            </svg>
          </div>
          <div className="card-content">
            <h3>Profile</h3>
            <p className="card-value">{user?.email}</p>
            <p className="card-description">{user?.city}, {user?.country}</p>
          </div>
        </div>
      </div>

      <BalanceDialog
        isOpen={isBalanceDialogOpen}
        currentBalance={user?.account_balance || 0}
        onClose={() => setIsBalanceDialogOpen(false)}
        onTransactionComplete={handleTransactionComplete}
      />
    </div>
  );
};
