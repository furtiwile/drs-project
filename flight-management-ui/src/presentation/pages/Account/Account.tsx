import { useState } from 'react';
import { useAuth } from '../../../application/context/AuthContext';
import { Input } from '../../shared/Input/Input';
import { Select } from '../../shared/Select/Select';
import { Button } from '../../shared/Button/Button';
import { Gender } from '../../../domain/enums/Gender';
import { AvatarUploadDialog } from './AvatarUploadDialog';
import './Account.css';

export const Account = () => {
  const { user } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [isAvatarDialogOpen, setIsAvatarDialogOpen] = useState(false);
  const [formData, setFormData] = useState({
    first_name: user?.first_name || '',
    last_name: user?.last_name || '',
    email: user?.email || '',
    birth_date: user?.birth_date || '',
    gender: user?.gender || Gender.OTHER,
    country: user?.country || '',
    city: user?.city || '',
    street: user?.street || '',
    house_number: user?.house_number || 0,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'house_number' ? parseInt(value) || 0 : value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsEditing(false);
  };

  const handleCancel = () => {
    setFormData({
      first_name: user?.first_name || '',
      last_name: user?.last_name || '',
      email: user?.email || '',
      birth_date: user?.birth_date || '',
      gender: user?.gender || Gender.OTHER,
      country: user?.country || '',
      city: user?.city || '',
      street: user?.street || '',
      house_number: user?.house_number || 0,
    });
    setIsEditing(false);
  };

  return (
    <div className="account-container">
      <div className="account-header">
        <h1>Account Settings</h1>
        <p>Manage your profile information</p>
      </div>

      <div className="account-card">
        <div className="account-profile">
          <div className="profile-avatar-large clickable" onClick={() => setIsAvatarDialogOpen(true)}>
            {user?.profile_picture ? (
              <img src={user.profile_picture} alt={user.first_name} />
            ) : (
              <span>{user?.first_name[0]}{user?.last_name[0]}</span>
            )}
            <div className="avatar-overlay">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="17 8 12 3 7 8"></polyline>
                <line x1="12" y1="3" x2="12" y2="15"></line>
              </svg>
            </div>
          </div>
          <div className="profile-info">
            <h2>{user?.first_name} {user?.last_name}</h2>
            <p className="profile-email">{user?.email}</p>
            <div className="profile-badges">
              <span className="badge badge-role">{user?.role}</span>
              <span className="badge badge-balance">Balance: ${user?.account_balance.toFixed(2)}</span>
            </div>
          </div>
        </div>

        <div className="divider" />

        <form onSubmit={handleSubmit} className="account-form">
          <div className="section-header">
            <h3>Personal Information</h3>
            {!isEditing && (
              <Button type="button" variant="secondary" onClick={() => setIsEditing(true)}>
                Edit Profile
              </Button>
            )}
          </div>

          <div className="form-grid">
            <Input
              type="text"
              name="first_name"
              label="First Name"
              value={formData.first_name}
              onChange={handleChange}
              disabled={!isEditing}
            />
            <Input
              type="text"
              name="last_name"
              label="Last Name"
              value={formData.last_name}
              onChange={handleChange}
              disabled={!isEditing}
            />
          </div>

          <Input
            type="email"
            name="email"
            label="Email"
            value={formData.email}
            onChange={handleChange}
            disabled={!isEditing}
          />

          <div className="form-grid">
            <Input
              type="date"
              name="birth_date"
              label="Birth Date"
              value={formData.birth_date}
              onChange={handleChange}
              disabled={!isEditing}
            />
            <Select
              name="gender"
              label="Gender"
              value={formData.gender}
              onChange={handleChange}
              disabled={!isEditing}
              options={[
                { value: Gender.MALE, label: 'Male' },
                { value: Gender.FEMALE, label: 'Female' },
                { value: Gender.OTHER, label: 'Other' }
              ]}
            />
          </div>

          <div className="section-header">
            <h3>Address</h3>
          </div>

          <div className="form-grid">
            <Input
              type="text"
              name="country"
              label="Country"
              value={formData.country}
              onChange={handleChange}
              disabled={!isEditing}
            />
            <Input
              type="text"
              name="city"
              label="City"
              value={formData.city}
              onChange={handleChange}
              disabled={!isEditing}
            />
          </div>

          <div className="form-grid">
            <Input
              type="text"
              name="street"
              label="Street"
              value={formData.street}
              onChange={handleChange}
              disabled={!isEditing}
            />
            <Input
              type="number"
              name="house_number"
              label="Number"
              value={formData.house_number}
              onChange={handleChange}
              disabled={!isEditing}
            />
          </div>

          {isEditing && (
            <div className="form-actions">
              <Button type="button" variant="secondary" onClick={handleCancel}>
                Cancel
              </Button>
              <Button type="submit">
                Save Changes
              </Button>
            </div>
          )}
        </form>
      </div>

      <AvatarUploadDialog
        isOpen={isAvatarDialogOpen}
        onClose={() => setIsAvatarDialogOpen(false)}
        onUploadSuccess={() => setIsAvatarDialogOpen(false)}
      />
    </div>
  );
};
