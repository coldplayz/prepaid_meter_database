#!/usr/bin/env python3
'''
Template class for table models.
'''

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from testdb import Base, Time, Num, Rel

engine = create_engine(
        'mysql+mysqldb://Bel2:44384439@localhost/testdb',
        pool_pre_ping=True)

Base.metadata.create_all(engine)
