#!/usr/bin/env python3
'''
Payments class for table models.
'''

from sqlalchemy import Computed, create_engine, Column, Integer, SmallInteger, String, Boolean, Date, Numeric, ForeignKey, func, cast, ForeignKeyConstraint, CheckConstraint
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
# from sqlalchemy.ext.declarative import declarative_base
from user import Base

'''
engine = create_engine(
        'mysql+mysqldb://Bel2:44384439@localhost/b2_prepaid_meter',
        pool_pre_ping=True)
'''

class Payment(Base):
    # Define table name
    __tablename__ = 'payments'

    ''' Define column-attributes.
        Format:
            col_name = Column(data_type, ...)
    '''
    paymentID = Column(Integer, primary_key=True)
    userID = Column(Integer, ForeignKey("users.userID", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    billID = Column(Integer, ForeignKey("bills.billID", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    transactionID = Column(Integer, ForeignKey("transactions.transactionID", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    amountPaid = Column(Integer)
    paymentDate = Column(Date, default=datetime.now().date)

    ''' Define table-level constraints.
        Format:
            __table_args__ = (comma-separated list of table constraints)
    '''
    # Code here
