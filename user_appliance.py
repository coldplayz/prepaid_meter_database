#!/usr/bin/env python3
'''
Class for appliance cost table model.
'''

from sqlalchemy import Computed, create_engine, Column, Integer, SmallInteger, String, Boolean, Date, Numeric, ForeignKey, func, cast, ForeignKeyConstraint, CheckConstraint
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
# from sqlalchemy.ext.declarative import declarative_base
from user import Base

engine = create_engine(
        'mysql+mysqldb://Bel2:PASSWORD@localhost/b2_prepaid_meter',
        pool_pre_ping=True)

Session = sessionmaker(bind=engine)

class UserAppliance(Base):
    # Define table name
    __tablename__ = 'userAppliances'

    ''' Define column-attributes.
        Format:
            col_name = Column(data_type, ...)
    '''
    applianceID = Column(Integer, ForeignKey("appliances.applianceID", ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    userID = Column(Integer, ForeignKey("users.userID", ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    transactionID = Column(Integer, ForeignKey("transactions.transactionID", ondelete='CASCADE', onupdate='CASCADE'))
    costAdjNum = Column(SmallInteger, nullable=False)
    adjustmentDate = Column(Date, default=datetime.now().date)
    applianceCount = Column(Numeric(10), nullable=False)

    ''' Define table-level constraints.
        Format:
            __table_args__ = (comma-separated list of table constraints)
    '''
    # Code here

    @classmethod
    def new_userAppliance(cls):
        ''' Creates and returns a new UserAppliance
        object representing a userAppliances record.
        '''
        from user import User
        from appliance import Appliance
        from transaction import Transaction

        # Collect attributes
        uID = input(f"Enter userID: ")
        aID = input("Enter applianceID: ")
        tID = input(f"Enter transactionID: ")
        caNum = input(f"Enter costAdjNum: ")
        aCount = input(f"Enter applianceCount: ")

        # Get related parent objects
        sess = Session()
        try:
            usr = sess.query(User).get(int(uID) if len(uID) > 0 else None)
            app = sess.query(Appliance).get(int(aID) if len(aID) > 0 else None)
            trn = sess.query(Transaction).get(int(tID) if len(tID) > 0 else None)
        finally:
            sess.close()

        # Create object
        userAppliance = cls(
                applianceID=(int(aID) if len(aID) > 0 else None),
                userID=(int(uID) if len(uID) > 0 else None),
                transactionID=(int(tID) if len(tID) > 0 else None),
                costAdjNum=(int(caNum) if len(caNum) > 0 else None),
                applianceCount=(int(aCount) if len(aCount) > 0 else None),
                user = usr,
                appliance = app,
                transaction = trn
                )

        return userAppliance

    @classmethod
    def is_completed(cls):
        ''' Check operation flag of model table.
        '''
        from flag import Flag
        sess = Session()

        try:
            # Get flag for users
            qobj = sess.query(Flag.flag).filter(Flag.operation == 'userAppliances')
            flag = qobj.scalar()
            if not flag:
                return True
        except Exception as e:
            raise e
        finally:
            sess.close()

        return False
