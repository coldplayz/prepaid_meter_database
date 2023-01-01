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

# Base.metadata.create_all(engine)

#time1 = Time()
#time2 = Time(created_on='2020-02-13')
n1 = Num(num1=45, num2=55)
n2 = Num(num1=37, num2=92)
r1 = Rel(phone='08103665556', numID=1)
r2 = Rel(numID=2)
r3 = Rel(numID=2)
r4 = Rel(numID=1)
r5 = Rel(numID=1, phone=None)
Session = sessionmaker(bind=engine)
sess = Session()

try:
    sess.add_all([n1, n2, r1, r2, r3, r4, r5])
    sess.commit()
except Exception as e:
    raise e
finally:
    sess.close()
