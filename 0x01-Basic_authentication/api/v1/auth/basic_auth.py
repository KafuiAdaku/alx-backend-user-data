#!/usr/bin/env python3
"""Basic authorization module"""
from .auth import Auth
import base64


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
