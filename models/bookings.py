#!/usr/bin/env python3
"""
A SQLAlchemy model named User for a database table named users
"""
import uuid 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, func
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

    booking_id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))
    email = Column(String(250), nullable=False)
    created_at = Column(String(250), nullable=True, default=get_current_time_in_nairobi())
    expected_date = Column(String(250), nullable=True, default="You will be updated")
    status = Column(String(250), nullable=True, default="Pending")