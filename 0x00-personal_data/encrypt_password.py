#!/usr/bin/env python3
"""hashing password using bcrypt"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password
    Args:
        password: password to be hashed

    Returns: hashed password as a byte string
    """
    pwd = password.encode()
    hashed = bcrypt.hashpw(pwd, bcrypt.gensalt())
    return hashed
