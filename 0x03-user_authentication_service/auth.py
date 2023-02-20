#!/usr/bin/env python3
""" define a _hash_password method """
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password):
    """ takes in password string arguments & returns bytes
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user

        Args:
            email: email address of the new user
            password: password of the new user

        Returns:
            The newly registered user object

         Raises:
            ValueError: if a user with this email is already registered
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            pass_word = _hash_password(password)
            user = self._db.add_user(email, pass_word)
            return user
        else:
            raise ValueError(f"User {email} already exists")
