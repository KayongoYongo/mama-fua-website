#!/usr/bin/env python3
"""
A SQLAlchemy model named User for a database table named users
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from models.nairobi_timezone import get_current_time_in_nairobi

Base = declarative_base()


class Bookings(Base):
    """This class is responsible for the creation of the user model

    Args:
        Base: The inherited declarative base

    Return:
        None
    """
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    created_at = Column(String(250), nullable=True, default=get_current_time_in_nairobi())
    pickup_date = Column(String(250), nullable=True)
    pickup_time = Column(String(250), nullable=True)
    delivery_time = Column(String(250), nullable=True)
    location = Column(String(250), nullable=True)
    expected_date = Column(String(250), nullable=True, default="You will be updated")
    status = Column(String(250), nullable=True, default="Pending")