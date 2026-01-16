import { useAuth } from '../../../application/context/AuthContext';
import { UserManagementSection } from '../../layouts/MainLayout/UserManagementSection';
import './UserManagement.css';

export const UserManagement = () => {
  const { user } = useAuth();

  if (!user) {
    return null;
  }

  return (
    <div className="user-management-page">
      <UserManagementSection currentUserId={user.user_id} />
    </div>
  );
};
