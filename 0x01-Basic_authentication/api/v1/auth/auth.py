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
        if path is None or excluded_paths is None or not excluded_paths:
            return True
        if path[-1] != "/":
            path += "/"
        if path in excluded_paths:
            return False
        return True

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
