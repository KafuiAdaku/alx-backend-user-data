#!/usr/bin/env python3
"""Session authentication with expiration module"""
from datetime import datetime, timedelta
from .session_auth import SessionAuth
import os


class SessionExpAuth(SessionAuth):
    """Session authentication with expiration"""
    def __init__(self):
        """Initialise constructor"""
        self.session_duration = int(os.getenv("SESSION_DURATION", 0))

    def create_session(self, user_id=None):
        """Create session ID
            Args:
                user_id (str): user id
            Returns: a newly created session id
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieves the user id using the session id
            Args:
                session_id (str): session id
            Returns: user id
        """
        if session_id is None:
            return None
        sess_dict = self.user_id_by_session_id.get(session_id)
        if sess_dict is None:
            return None
        if self.session_duration <= 0:
            return sess_dict.get("user_id")
        if not sess_dict.get("created_at"):
            return None
        end_time = sess_dict.get("created_at") + \
            timedelta(seconds=self.session_duration)
        if end_time < datetime.now():
            return None
        return sess_dict.get("user_id")
