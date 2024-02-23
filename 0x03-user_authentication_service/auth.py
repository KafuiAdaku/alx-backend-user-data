#!/usr/bin/env python3
"""Authentication module"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


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


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        """Class constructor"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user
            Args:
                email (str): user email
                password (str): user password

            Returns: A `User` object
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hash_pwd = _hash_password(password)
            new_user = self._db.add_user(email, hash_pwd)
            return new_user
