#!/usr/bin/env python3
'''
Module for creating tables from models.
'''

from sqlalchemy import create_engine
from user import Base, User
from appliance import Appliance
from user_appliance import UserAppliance
from transaction import Transaction
from bill import Bill
from payment import Payment
from flag import Flag

engine = create_engine(
        'mysql+mysqldb://Bel2:44384439@localhost/b2_prepaid_meter',
        pool_pre_ping=True)

Base.metadata.create_all(engine)
