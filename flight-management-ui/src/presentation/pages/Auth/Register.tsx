import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../../application/context/AuthContext';
import { Input } from '../../shared/Input/Input';
import { Select } from '../../shared/Select/Select';
import { Button } from '../../shared/Button/Button';
import { Gender } from '../../../domain/enums/Gender';
import './Auth.css';

export const Register = () => {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    birth_date: '',
    gender: Gender.OTHER,
    country: '',
    city: '',
    street: '',
    house_number: 0,
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'house_number' ? parseInt(value) || 0 : value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await register(formData);
      navigate('/');
    } catch (err: any) {
      setError(err.response?.data?.message || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card auth-card-large">
        <div className="auth-header">
          <h1>Create Account</h1>
          <p>Join our flight management platform</p>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-row">
            <Input
              type="text"
              name="first_name"
              label="First Name"
              value={formData.first_name}
              onChange={handleChange}
              required
            />
            <Input
              type="text"
              name="last_name"
              label="Last Name"
              value={formData.last_name}
              onChange={handleChange}
              required
            />
          </div>

          <Input
            type="email"
            name="email"
            label="Email"
            value={formData.email}
            onChange={handleChange}
            required
            autoComplete="email"
          />

          <Input
            type="password"
            name="password"
            label="Password"
            value={formData.password}
            onChange={handleChange}
            required
            autoComplete="new-password"
          />

          <div className="form-row">
            <Input
              type="date"
              name="birth_date"
              label="Birth Date"
              value={formData.birth_date}
              onChange={handleChange}
              required
            />
            <Select
              name="gender"
              label="Gender"
              value={formData.gender}
              onChange={handleChange}
              options={[
                { value: Gender.MALE, label: 'Male' },
                { value: Gender.FEMALE, label: 'Female' },
                { value: Gender.OTHER, label: 'Other' }
              ]}
              required
            />
          </div>

          <div className="form-row">
            <Input
              type="text"
              name="country"
              label="Country"
              value={formData.country}
              onChange={handleChange}
              required
            />
            <Input
              type="text"
              name="city"
              label="City"
              value={formData.city}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-row">
            <Input
              type="text"
              name="street"
              label="Street"
              value={formData.street}
              onChange={handleChange}
              required
            />
            <Input
              type="number"
              name="house_number"
              label="Number"
              value={formData.house_number}
              onChange={handleChange}
              required
            />
          </div>

          {error && <div className="error-box">{error}</div>}

          <Button type="submit" fullWidth disabled={loading}>
            {loading ? 'Creating account...' : 'Sign Up'}
          </Button>
        </form>

        <div className="auth-footer">
          Already have an account? <Link to="/login">Sign in</Link>
        </div>
      </div>
    </div>
  );
};
