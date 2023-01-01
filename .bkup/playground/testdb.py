#!/usr/bin/env python3
'''
Template class for table models.
'''

from sqlalchemy import Computed, Column, Integer, SmallInteger, String, Boolean, Date, DateTime, ForeignKey, func, cast, ForeignKeyConstraint, CheckConstraint
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
# from user import Base

'''
engine = create_engine(
        'mysql+mysqldb://{}:{}@localhost/{}'.format(
            sys.argv[1], sys.argv[2], sys.argv[3]) , pool_pre_ping=True)
'''

Base = declarative_base()

class Time(Base):
    # Define table name
    __tablename__ = 'dates'

    ''' Define column-attributes.
        Format:
            col_name = Column(data_type, ...)
    '''
    id = Column(Integer(), primary_key=True)
    created_on = Column(Date, default=datetime.now().date)

    ''' Define table-level constraints.
        Format:
            __table_args__ = (comma-separated list of table constraints)
    '''
    # Code here

class Num(Base):
    __tablename__ = 'nums'
    id = Column(Integer(), primary_key=True)
    num1 = Column(Integer())
    num2 = Column(Integer())
    num3 = Column(Integer(), Computed('num1 + num2', persisted=True))
    num4 = Column(Integer, default=num1 * num2)
    num5 = Column(Integer, default=num1 - num2, onupdate=num1 - num2)
    rels = relationship("Rel", backref='num', cascade="all, delete-orphan")


class Rel(Base):
    __tablename__ = 'rels'
    __table_args__ = (CheckConstraint('char_length(phone) = 11', name='phone_check'),)

    id = Column(Integer(), primary_key=True)
    numID = Column(Integer, ForeignKey('nums.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    phone = Column(String(11))

    #print(type(__table_args__))
