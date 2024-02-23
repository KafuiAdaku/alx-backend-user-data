#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Saves  a `User` object to the database
            Args:
                email (str): user email
                hashed_password (str): user hashed password
            Returns: User object
        """
        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
            return user
        except Exception:
            self._session.rollback()
            user = None
        return user

    def find_user_by(self, **kwargs) -> User:
        """Returns a `User` object"""
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
            return user
        except NoResultFound:
            raise
        except InvalidRequestError:
            raise

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates an already existing

            Args:
                user_id (int): user id
                kwargs (dict): arbitrary keyword arguments

            Returns: None
        """
        try:
            user = self._session.query(User).filter_by(id=user_id).one()
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise ValueError
            self._session.commit()
        except NoResultFound:
            raise
