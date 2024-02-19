#!/usr/bin/env python3
"""API management module"""
from flask import request
from typing import List, TypeVar
import fnmatch
import os


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
        exluded_paths = [pth + "/" if pth[-1] != "/" else pth
                         for pth in excluded_paths]
        for pth in excluded_paths:
            if fnmatch.fnmatch(path, pth):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization header
            Args:
                request: Flask request object

            Returns: None
        """
        if request is None:
            return None
        if not request.headers.get("Authorization"):
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """current user
            Args:
                request : Flask request object

                Returns: None
        """
        # if request is None:
        #     return None
        # header = request.headers.get("Authorization")
        # if header:
        #     return header
        return None

    def session_cookie(self, request=None):
        """session cookie
            Args:
                request : Flask request object

            Returns: None if no cookie or the value of the cookie
        """
        if request is None:
            return None
        session_name = os.getenv("SESSION_NAME")
        if not request.cookies.get(session_name):
            return None
        return request.cookies.get(session_name)
