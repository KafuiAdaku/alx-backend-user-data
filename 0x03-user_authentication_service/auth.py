#!/usr/bin/env python3
"""Authentication module"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hashes a password
        Args:
            password (str): password

        Returns (bytes): hashed passowrd
    """
    encoded_password = password.encode()
    hash_pwd = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
    return hash_pwd
