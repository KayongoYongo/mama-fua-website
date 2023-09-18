#!/usr/bin/env python3
"""A function that encrypts a password
"""
from models.user import User
from typing import Union
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
from uuid import uuid4
from db import DB


def _hash_password(password: str) -> str:
    """
    A method for hashing out a password

    Args:
        Password: The string to be hashed out

    Return:
        The password in byte format
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """Generate uuid
    Args:
        None

    Return:
        string
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """A method that initializes the DB object
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> Union[None, User]:
        """
        A method for registering users.

        Args:
            email: The email of the user
            password: The password of the user

        Return:
            None or user object
        """
        
        try:
            # find the user with the given email
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        else:
            raise ValueError('User {} already exists'.format(email))
        
    def valid_login(self, email: str, password: str) -> bool:
        """
        This function checks if the log in is valid.

        Args:
            email: The users email
            password: The users password

        Return:
            True or False
        """
        try:
            # find the user with the given email
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        # check the validity of the password and returns true
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """
        This function creates a session ID

        Args:
            email: The email that will be assigned to a session

        Return:
            A string which is the session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        else:
            user.session_id = _generate_uuid()
            return user.session_id

    def get_user_from_session_id(self, session_id):
        """
        This function finds the user by session ID

        Args:
            session_id: The identification of the session

        Return:
            None or User
        """
        if session_id is None:
            None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        else:
            return user

    def destroy_session(self, user_id):
        """
        This function destroys the current session of a user

        Args:
            user_id: The ID of the current user

        Return:
            None
        """
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        else:
            user.session_id = None
            return None