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