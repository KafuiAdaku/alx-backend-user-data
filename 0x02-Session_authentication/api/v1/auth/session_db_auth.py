#!/usr/bin/env python3
"""Database session authentication module"""
from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """Database session authentication class"""
    def create_session(self, user_id=None):
        """Creates and stores a new instance of `UserSession`"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns the user_id by requesting UserSession in the database"""
        if session_id is None:
            return None
        user_sessions = UserSession.search({"session_id": session_id})
        if not user_sessions:
            return None
        user_session = user_sessions[0]  # session id is unique
        if self.session_duration <= 0:
            return user_session.user_id
        if not user_session.created_at:
            return None
        end_time = user_session.created_at + \
            timedelta(seconds=self.session_duration)
        if end_time < datetime.now():
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """Deletes the user session / logout"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_sessions = UserSession.search({"session_id": session_id})
        if not user_sessions:
            return False
        user_session[0].remove()
        return True
