import { useState, useRef } from 'react';
import { userService } from '../../../infrastructure/services/userService';
import { useAuth } from '../../../application/context/AuthContext';
import './AvatarUploadDialog.css';

interface AvatarUploadDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onUploadSuccess: () => void;
}

export const AvatarUploadDialog = ({ isOpen, onClose, onUploadSuccess }: AvatarUploadDialogProps) => {
  const { refreshUser } = useAuth();
  const [preview, setPreview] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate file type
    if (!file.type.startsWith('image/')) {
      alert('Please select a valid image file');
      return;
    }

    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      alert('Image size must be less than 5MB');
      return;
    }

    const reader = new FileReader();
    reader.onload = (event) => {
      setPreview(event.target?.result as string);
    };
    reader.readAsDataURL(file);
  };

  const handleSet = async () => {
    if (!preview) return;

    setIsLoading(true);
    try {
      await userService.updateProfilePicture(preview);
      await refreshUser();
      alert('Profile picture updated successfully!');
      setPreview(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
      onUploadSuccess();
      onClose();
    } catch {
      alert('Failed to update profile picture. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancel = () => {
    setPreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="avatar-upload-overlay" onClick={handleCancel}>
      <div className="avatar-upload-dialog" onClick={e => e.stopPropagation()}>
        <div className="dialog-header">
          <h2>Change Profile Picture</h2>
          <button className="close-btn" onClick={handleCancel}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <div className="dialog-content">
          {!preview ? (
            <div className="upload-area">
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleFileSelect}
                style={{ display: 'none' }}
              />
              <button
                type="button"
                className="upload-button"
                onClick={() => fileInputRef.current?.click()}
              >
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                  <polyline points="17 8 12 3 7 8"></polyline>
                  <line x1="12" y1="3" x2="12" y2="15"></line>
                </svg>
                <p>Click to select an image</p>
                <p className="upload-hint">PNG, JPG, GIF up to 5MB</p>
              </button>
            </div>
          ) : (
            <div className="preview-area">
              <img src={preview} alt="Preview" className="preview-image" />
              <p className="preview-label">Preview</p>
            </div>
          )}
        </div>

        <div className="dialog-actions">
          <button className="btn-cancel" onClick={handleCancel} disabled={isLoading}>
            {preview ? 'Change' : 'Cancel'}
          </button>
          {preview && (
            <button className="btn-set" onClick={handleSet} disabled={isLoading}>
              {isLoading ? 'Uploading...' : 'Set Picture'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
