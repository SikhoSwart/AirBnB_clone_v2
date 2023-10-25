#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base

# SQLAlchemy modules
from sqlalchemy import Column
from sqlalchemy import String


class User(BaseModel, Base):
    """
    Defines a class User
    Attributes:
        __tablename__ (str): Users MySQL table name
    """
    __tablename__ = 'users'

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))
