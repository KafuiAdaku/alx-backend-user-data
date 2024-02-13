#!/usr/bin/env python3
"""API management module"""
from flask import request
from typing import List, TypeVar

class Auth:
    """Manage API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require authentication
            Args:
                path (str): url path
                exluded_paths (list):

            Returns: bool
        """
        return False


    def authorization_header(self, request=None) -> str:
        """authorization header
            Args:
                request: Flask request object

            Returns: None
        """
        return None


    def current_user(self, request=None) -> TypeVar('User'):
        """current user
            Args:
                request : Flask request object

                Returns: None
        """
        return None
