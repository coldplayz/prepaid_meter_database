#!/usr/bin/env python3
'''
Table for storing operations flags.
'''

from sqlalchemy import Computed, create_engine, Column, Integer, SmallInteger, String, Boolean, DateTime, Numeric, ForeignKey, func, cast, ForeignKeyConstraint, CheckConstraint
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
#from sqlalchemy.ext.declarative import declarative_base
#from user import Base
from flag import Flag

engine = create_engine(
        'mysql+mysqldb://Bel2:44384439@localhost/b2_prepaid_meter',
        pool_pre_ping=True)

# Create objects
op1 = Flag(operation='user')
op2 = Flag(operation='appliance')
op3 = Flag(operation='transaction')
op4 = Flag(operation='userAppliance')
op5 = Flag(operation='bill')
op6 = Flag(operation='payment')

Session = sessionmaker(bind=engine)
sess = Session()

try:
    sess.add_all([op1, op2, op3, op4, op5, op6])
    sess.commit()
except Exception as e:
    raise e
finally:
    sess.close()
