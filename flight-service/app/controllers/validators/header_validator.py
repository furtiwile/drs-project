"""
Header validation utilities for controllers
"""
from typing import Optional


def validate_user_id_header(user_id_str: Optional[str]) -> int:
    """
    Validates and converts user-id header to integer.
    
    Args:
        user_id_str: The user-id header value
        
    Returns:
        int: The validated user ID
        
    Raises:
        ValueError: If header is missing or invalid
    """
    if not user_id_str:
        raise ValueError({'error': 'user-id header is required'})
    
    try:
        user_id = int(user_id_str)
        if user_id < 1:
            raise ValueError({'error': 'user-id must be a positive integer'})
        return user_id
    except (ValueError, TypeError):
        raise ValueError({'error': 'Invalid user-id in header'})


def validate_admin_id_header(admin_id_str: Optional[str]) -> int:
    """
    Validates and converts admin-id header to integer.
    
    Args:
        admin_id_str: The admin-id header value
        
    Returns:
        int: The validated admin ID
        
    Raises:
        ValueError: If header is missing or invalid
    """
    if not admin_id_str:
        raise ValueError({'error': 'admin-id header is required'})
    
    try:
        admin_id = int(admin_id_str)
        if admin_id < 1:
            raise ValueError({'error': 'admin-id must be a positive integer'})
        return admin_id
    except (ValueError, TypeError):
        raise ValueError({'error': 'Invalid admin-id in header'})


def validate_role_header(role_str: Optional[str]) -> str:
    """
    Validates role header.
    
    Args:
        role_str: The role header value
        
    Returns:
        str: The validated role
        
    Raises:
        ValueError: If header is missing or invalid
    """
    if not role_str:
        raise ValueError({'error': 'Role header is required'})
    
    valid_roles = ['ADMIN', 'MANAGER', 'USER']
    role_upper = role_str.upper()
    
    if role_upper not in valid_roles:
        raise ValueError({'error': f'Invalid role. Must be one of: {", ".join(valid_roles)}'})
    
    return role_upper
