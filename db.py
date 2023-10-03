#!/usr/bin/env python3
"""DB module
"""
# from models.user import User, Base
# from models.bookings import Bookings, Base
from models.all_models import User, Bookings, Base
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        # mysql_url = 'mysql+mysqldb://end_user:password@localhost:3306/mama_fua'
        mysql_url ="sqlite:///a.db"
        self._engine = create_engine(mysql_url, echo=False)
        
        """
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        """
        
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str, first_name:str, second_name: str, phone_number: str)  -> User:
        """
        Add a new user to the database.

        Args:
            email: The email of the user
            hashed_password: Hashed password of the user

        Returns:
            User: The newly created user object.
        """

        user = User(email=email, hashed_password=hashed_password, first_name=first_name, second_name=second_name, phone_number=phone_number)
        self._session.add(user)
        self._session.commit()
        return user
    
    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by given filter arguments

        Args:
            **kwargs: Arbitrary keyword arguments to filter the user.

        Returns:
            User: The found user object.

        Raises:
            NoResultFound: When no user is found
            MultipleResultsFOund: When multiple users match the filter
            InvalidRequestError: When Invalid query arguments are passed
        """
        if not kwargs:
            raise InvalidRequestError

        user = self._session.query(User).filter_by(**kwargs).first()

        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        A method that takes as argument a required user_id integer
        and arbitrary keyword arguments, and returns None

        Args:
            user_id (int): The user's ID

        Return:
            Returns None or arbitray key worded argments
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError
            setattr(user, key, value)

        self._session.commit()
        return None
    
    def add_booking(self, email: str) -> Bookings:
        """
        Add a new booking to the database.

        Args:
            email: The email of the user

        Returns:
            User: The newly created booking object.
        """
        booking = Bookings(email=email)
        self._session.add(booking)
        self._session.commit()
        return booking
    
    def find_booking_by(self, **kwargs) -> Bookings:
        """
        Find a booking by given filter arguments

        Args:
            **kwargs: Arbitrary keyword arguments to filter the user.

        Returns:
            User: The found user object.

        Raises:
            NoResultFound: When no user is found
            MultipleResultsFOund: When multiple users match the filter
            InvalidRequestError: When Invalid query arguments are passed
        """
        if not kwargs:
            raise InvalidRequestError

        booking = self._session.query(Bookings).filter_by(**kwargs).first()

        if booking is None:
            raise NoResultFound
        return booking
    
    def find_all_bookings_by(self, **kwargs) -> Bookings:
        """
        Find a booking by given filter arguments

        Args:
            **kwargs: Arbitrary keyword arguments to filter the user.

        Returns:
            User: The found user object.

        Raises:
            NoResultFound: When no user is found
            MultipleResultsFOund: When multiple users match the filter
            InvalidRequestError: When Invalid query arguments are passed
        """
        if not kwargs:
            raise InvalidRequestError

        bookings = self._session.query(Bookings).filter_by(**kwargs).all()

        if bookings is None:
            raise NoResultFound
        return bookings
    
    def update_booking(self, email: str, **kwargs) -> None:
        """
        A method that takes as argument a required user_id integer
        and arbitrary keyword arguments, and returns None

        Args:
            user_id (int): The user's ID

        Return:
            Returns None or arbitray key worded argments
        """
        booking = self.find_booking_by(email=email)
        for key, value in kwargs.items():
            if not hasattr(booking, key):
                raise ValueError
            setattr(booking, key, value)

        self._session.commit()
        return None    