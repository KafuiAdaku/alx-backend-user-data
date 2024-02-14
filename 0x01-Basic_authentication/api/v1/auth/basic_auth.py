#!/usr/bin/env python3
"""Basic authorization module"""
from .auth import Auth


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
