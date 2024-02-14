#!/usr/bin/env python3
"""Basic authorization module"""
from .auth import Auth
import base64
from typing import TypeVar


class BasicAuth(Auth):
    """Basic Authorization class"""
    def extract_base64_authorization_header(self, authorization_header:
                                            str) -> str:
        """Extract base64 authorization header
            Args:
                authorization_header (str): base64 encoded string
            Returns: str
        """
        if authorization_header is None or \
                not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split()[1].strip()

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """Decode base64 authorization
            Args:
                base64_authorization_header (str): base64 code

            Returns: str
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode("UTF-8")
        except Exception as e:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """Extract user credentials
            Args:
                decoded_base64_authorization_header (str): decoded auth header

            Returns: Tuple[str]
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(":"))

    def user_object_from_credentials(self, user_email: str, user_pwd:
                                     str) -> TypeVar('User'):
        """Creates and returns a `User` instance object from email and password
            Args:
                user_email (str): user email
                user_pwd (str): user password

            Returns: User object
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            from models.user import User
            users = User.search({"email": user_email})
            if not users:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception as e:
            return None
