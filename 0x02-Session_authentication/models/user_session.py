#!/usr/bin/env python3
"""User session Database"""
from .base import Base


class UserSession(Base):
    """User session"""
    def __init__(self, *args: list, **kwargs: dict):
        """Initialise constructor"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
