#!/usr/bin/env python3
"""hashing password using bcrypt"""
import bcrypt


def hash_password(password: str) -> str:
    """Hashes a password
    Args:
        password: password to be hashed

    Returns: hashed password
    """
    pwd = password.encode('utf-8')
    hashed = bcrypt.hashpw(pwd, bcrypt.gensalt())
    if bcrypt.checkpw(pwd, hashed):
        return hashed
