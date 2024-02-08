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


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks the validity of a password

        Args:
            hashed_password (byte) : byte stringed hashed password
            password (str): password to be checked

        Returns (bool): boolean
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
