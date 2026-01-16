import { useEffect, useState } from "react";
import "./UserManagementSection.css";
import { userService } from "../../../infrastructure/services/userService";
import type { User } from "../../../domain/models/User";
import { Role } from "../../../domain/enums/Role";

interface UserManagementSectionProps {
  currentUserId: number;
}

export const UserManagementSection = ({ currentUserId }: UserManagementSectionProps) => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [updatingUserId, setUpdatingUserId] = useState<number | null>(null);

  useEffect(() => {
    userService.getAllUsers()
      .then(setUsers)
      .catch(() => alert("Failed to fetch users."))
      .finally(() => setLoading(false));
  }, []);

  const handleRoleChange = async (userId: number, newRole: string) => {
    setUpdatingUserId(userId);
    try {
      await userService.updateUserRole(userId, newRole as Role);
      setUsers(users => users.map(u => u.user_id === userId ? { ...u, role: newRole as Role } : u));
    } catch {
      alert("Failed to update user role.");
    } finally {
      setUpdatingUserId(null);
    }
  };

  const handleRoleSelectFocus = (userRole: string) => {
    if (userRole === 'ADMINISTRATOR') {
      alert('You can not change another administrators. Contact Nikola Kovac or Radoman Dakic');
    }
  };

  const handleDelete = async (userId: number) => {
    const userToDelete = users.find(u => u.user_id === userId);
    if (userToDelete?.role === 'ADMINISTRATOR') {
      alert('You can not change another administrators. Contact Nikola Kovac or Radoman Dakic');
      return;
    }
    setUpdatingUserId(userId);
    try {
      await userService.deleteUser(userId);
      setUsers(users => users.filter(u => u.user_id !== userId));
    } catch {
      alert("Failed to delete user.");
    } finally {
      setUpdatingUserId(null);
    }
  };

  if (loading) return <section className="user-management-section"><div className="loading">Loading users...</div></section>;

  const filteredUsers = users.filter(u => u.user_id !== currentUserId);

  return (
    <section className="user-management-section">
      <div className="section-header">
        <h2>User Management</h2>
      </div>
      {filteredUsers.length === 0 ? (
        <div className="empty-state">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
            <circle cx="9" cy="7" r="4"></circle>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
          </svg>
          <p>No users to manage</p>
        </div>
      ) : (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Role</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredUsers.map(user => (
                <tr key={user.user_id}>
                  <td>{user.first_name} {user.last_name}</td>
                  <td>{user.email}</td>
                  <td>
                    <select
                      value={user.role}
                      onChange={e => handleRoleChange(user.user_id, e.target.value)}
                      onFocus={() => handleRoleSelectFocus(user.role)}
                      disabled={updatingUserId === user.user_id || user.role === 'ADMINISTRATOR'}
                    >
                      {Object.values(Role).filter(role => role !== 'ADMINISTRATOR').map(role => (
                        <option key={role} value={role}>{role}</option>
                      ))}
                      {user.role === 'ADMINISTRATOR' && (
                        <option value='ADMINISTRATOR'>ADMINISTRATOR</option>
                      )}
                    </select>
                  </td>
                  <td>
                    <button
                      onClick={() => handleDelete(user.user_id)}
                      disabled={updatingUserId === user.user_id}
                      className="btn-delete"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
};
