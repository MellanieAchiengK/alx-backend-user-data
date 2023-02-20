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
        """Add a user to the database

        Args:
            email: an email address for the user
            hashed_password: the user's hashed password

        Returns:
            a User object
        """
        new_user = User(email=email, hashed_password=hashed_password)

        self._session.add(new_user)

        self._session.commit()

        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find user by arbitrary keyword arguments

        Args:
            kwargs: any keyword arguments to filter the users

        Returns:
            a User object

        Raises:
            NoResultFound: if no results are found
            InvalidRequestError: if wrong query arguments are passed
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound("No users matching kwargs were found")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query arguments were passed")
        else:
            return user

    def update_user(self, user_id, **kwargs):
        """Update a user in the database

        Args:
            user_id: the id of the user to update
            **kwargs: key-value arguments for updating the user's attributes
                    where the keys are the attributes' names and the values
                    are their new values

        Raises:
            ValueError: if an argument that does not correspond to a user
            attribute is passed
            NoResultFound: if no results are found
            InvalidRequestError: if wrong query arguments are passed
        """
        user = self.find_user_by(id=user_id)
        for attr, value in kwargs.items():
            if hasattr(user, attr):
                setattr(user, attr, value)
            else:
                raise ValueError(f"Invalid parameter '{attr}'")

        self._session.commit()
