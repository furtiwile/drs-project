import { useState, useRef, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../../application/context/AuthContext';
import './MainLayout.css';

export const MainLayout = ({ children }: { children: React.ReactNode }) => {
  const { user, logout } = useAuth();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setDropdownOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

	return (
		<div className="layout">
			<header className="header">
				<div className="header-content">
					<div className="logo">
						<Link to="/">Flight Manager</Link>
					</div>
					<div className="header-right">
						<div className="user-menu" ref={dropdownRef}>
							<button
								className="user-button"
								onClick={() => setDropdownOpen(!dropdownOpen)}
							>
								<div className="user-avatar">
									{user?.profile_picture ? (
										<img src={user.profile_picture} alt={user.first_name} />
									) : (
										<span>
											{user?.first_name[0]}
											{user?.last_name[0]}
										</span>
									)}
								</div>
								<span className="user-name">
									{user?.first_name} {user?.last_name}
								</span>
								<svg
									className={`chevron ${dropdownOpen ? "open" : ""}`}
									width="20"
									height="20"
									viewBox="0 0 20 20"
									fill="currentColor"
								>
									<path
										fillRule="evenodd"
										d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
										clipRule="evenodd"
									/>
								</svg>
							</button>
							{dropdownOpen && (
								<div className="dropdown">
									<div className="dropdown-header">
										<div className="dropdown-user-info">
											<span className="dropdown-name">
												{user?.first_name} {user?.last_name}
											</span>
											<span className="dropdown-email">{user?.email}</span>
											<span className="dropdown-role">{user?.role}</span>
										</div>
									</div>
									<div className="dropdown-divider" />
									
									{user?.role === 'ADMINISTRATOR' && (
										<>
											<Link
												to="/admin/dashboard"
												className="dropdown-item"
												onClick={() => setDropdownOpen(false)}
											>
												<svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
													<path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />
												</svg>
												Admin Dashboard
											</Link>
											
											<Link
												to="/admin/reports"
												className="dropdown-item"
												onClick={() => setDropdownOpen(false)}
											>
												<svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
													<path d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" />
												</svg>
												Reports & Analytics
											</Link>
										</>
									)}
									
									{user?.role === 'MANAGER' && (
										<Link
											to="/manager/dashboard"
											className="dropdown-item"
											onClick={() => setDropdownOpen(false)}
										>
											<svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
												<path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />
											</svg>
											Manager Dashboard
										</Link>
									)}
									
									<Link
										to="/flights"
										className="dropdown-item"
										onClick={() => setDropdownOpen(false)}
									>
										<svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
											<path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
										</svg>
										Available Flights
									</Link>
									
									<Link
										to="/bookings"
										className="dropdown-item"
										onClick={() => setDropdownOpen(false)}
									>
										<svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
											<path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
											<path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd" />
										</svg>
										My Bookings
									</Link>
									
									<div className="dropdown-divider" />
									
									<Link
										to="/account"
										className="dropdown-item"
										onClick={() => setDropdownOpen(false)}
									>
										<svg
											width="20"
											height="20"
											viewBox="0 0 20 20"
											fill="currentColor"
										>
											<path
												fillRule="evenodd"
												d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"
												clipRule="evenodd"
											/>
										</svg>
										Account Settings
									</Link>
									{user?.role === 'ADMINISTRATOR' && (
										<>
											<div className="dropdown-divider" />
											<Link
												to="/users"
												className="dropdown-item"
												onClick={() => setDropdownOpen(false)}
											>
												<svg
													width="20"
													height="20"
													viewBox="0 0 20 20"
													fill="currentColor"
												>
													<path
														fillRule="evenodd"
														d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z"
														clipRule="evenodd"
													/>
												</svg>
												Manage Users
											</Link>
										</>
									)}
									<div className="dropdown-divider" />
									<button
										className="dropdown-item danger"
										onClick={handleLogout}
									>
										<svg
											width="20"
											height="20"
											viewBox="0 0 20 20"
											fill="currentColor"
										>
											<path
												fillRule="evenodd"
												d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z"
												clipRule="evenodd"
											/>
										</svg>
										Logout
									</button>
								</div>
							)}
						</div>
					</div>
				</div>
			</header>
			<main className="main-content">{children}</main>
		</div>
	);
};
