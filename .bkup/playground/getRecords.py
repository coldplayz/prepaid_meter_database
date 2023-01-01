#!/usr/bin/env python3
'''
Template class for table models.
'''

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from testdb import Base, Time, Num

engine = create_engine(
        'mysql+mysqldb://Bel2:44384439@localhost/testdb',
        pool_pre_ping=True)

# Base.metadata.create_all(engine)

#time1 = Time()
#time2 = Time(created_on='2020-02-13')
#n1 = Num(num1=45, num2=55)
#n2 = Num(num1=37, num2=92)
Session = sessionmaker(bind=engine)
sess = Session()

try:
    qobj = sess.query(Num)
except Exception as e:
    raise e
finally:
    pass
    #sess.close()
