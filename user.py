#!/usr/bin/env python3
'''
User class for table models.
'''

from sqlalchemy import Computed, create_engine, Column, Integer, SmallInteger, String, Boolean, DateTime, Numeric, ForeignKey, func, cast, ForeignKeyConstraint, CheckConstraint
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from decimal import Decimal
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(
        'mysql+mysqldb://Bel2:PASSWORD@localhost/b2_prepaid_meter',
        pool_pre_ping=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()

class User(Base):
    # Define table name
    __tablename__ = 'users'

    ''' Define column-attributes.
        Format:
            col_name = Column(data_type, ...)
    '''
    userID = Column(Integer(), primary_key=True)
    userName = Column(String(50), nullable=False)
    whatsapp = Column(String(11))
    phone_1 = Column(String(11))
    phone_2 = Column(String(11))
    sex = Column(String(1), nullable=False)
    roomIdx = Column(SmallInteger(), nullable=False)
    currRate = Column(Numeric(5, 2), default=0)
    isResident = Column(Boolean, default=True)

    # Relationships
    userBills = relationship("Bill", backref='user', cascade="all, delete-orphan")
    userAppliances = relationship("UserAppliance", backref="user", cascade="all, delete-orphan")
    userPayments = relationship("Payment", backref="user", cascade="all, delete-orphan")

    ''' Define table-level constraints.
        Format:
            __table_args__ = (comma-separated list of table constraints)
    '''
    __table_args__ = (
            CheckConstraint(
                'char_length(whatsapp) = 11',
                name='check_whatsapp'),
            CheckConstraint(
                'char_length(phone_1) = 11',
                name='check_phone_1'),
            CheckConstraint(
                'char_length(phone_2) = 11',
                name='check_phone_2'))


    @classmethod
    def new_user(cls):
        ''' Creates and returns a new User object representing a users record.
        '''

        # Collect attributes
        uname = input("Enter userName: ")
        wapp = input(f"Enter {uname if len(uname) > 0 else 'userName'}'s whatsapp: ")
        phone1 = input(f"Enter {uname if len(uname) > 0 else 'userName'}'s phone_1: ")
        phone2 = input(f"Enter {uname if len(uname) > 0 else 'userName'}'s phone_2: ")
        sx = input(f"Enter {uname if len(uname) > 0 else 'userName'}'s sex: ")
        rmIdx = input(f"Enter {uname if len(uname) > 0 else 'userName'}'s roomIdx (0-based): ")
        isRsdnt = input(f"Is {uname if len(uname) > 0 else 'userName'} still resident? True/False: ")
        if isRsdnt == 'True':
            isRsdnt = True
        else:
            isRsdnt = False if isRsdnt == 'False' else None

        # Create object
        user = cls(
                userName=(uname if len(uname) > 0 else None),
                whatsapp=(wapp if len(wapp) > 0 else None),
                phone_1=(phone1 if len(phone1) > 0 else None),
                phone_2=(phone2 if len(phone2) > 0 else None),
                sex=(sx if len(sx) > 0 else None),
                roomIdx=(int(rmIdx) if len(rmIdx) > 0 else None),
                isResident=isRsdnt
                )

        return user

    @classmethod
    def is_completed(cls):
        ''' Check operation flag of model table.
        '''
        from flag import Flag
        sess = Session()

        try:
            # Get flag for users
            qobj = sess.query(Flag.flag).filter(Flag.operation == 'users')
            flag = qobj.scalar()
            if not flag:
                return True
        except Exception as e:
            raise e
        finally:
            sess.close()

        return False

    @classmethod
    def calc_rates(cls):
        ''' [Re]calculate each user's currRate for determining share of recharge.
        '''
        from appliance import Appliance
        from transaction import Transaction
        from user_appliance import UserAppliance

        sess = Session()

        try:
            # Get all resident users records
            uRecs = sess.query(cls).filter(cls.isResident == True).all()
            uCosts = []  # will contain costs matching for each user record

            # Iterate over uRecs; each uRec represents a User
            for uRec in uRecs:
                uID = uRec.userID  # save each user id
                # Get latest transactionID for user, uRec
                tID = sess.query(func.max(UserAppliance.transactionID)).filter(UserAppliance.userID == uID).scalar()
                # Use uID and tID to get latest userAppliance records for user
                uaRecs = sess.query(UserAppliance).filter(UserAppliance.userID == uID, UserAppliance.transactionID == tID).all()
                cSum = Decimal(0)  # for summing user's adjusted costs
                
                # Iterate over uaRecs
                for uaRec in uaRecs:
                    # Save applianceID
                    aID = uaRec.applianceID
                    # Fetch appliance record
                    aRec = sess.query(Appliance).filter(Appliance.applianceID == aID).one()
                    # Get cost for a used appliance
                    appCost = aRec.adjRelCost * uaRec.applianceCount
                    cSum += appCost
                # Append user's total cost to uCosts list
                uCosts.append(cSum)
            # Save sum of uCosts values
            tcSum = sum(uCosts)
            # Create user rates list
            uRates = [x / tcSum for x in uCosts]

            # Update users.currRate
            for i in range(len(uRecs)):
                uRecs[i].currRate = uRates[i]

            # Add and commit
            sess.add_all(uRecs)
            sess.commit()
        finally:
            sess.close()

    @classmethod
    def residentUsers(cls):
        ''' Fetch number of resident users.
        '''
        sess = Session()
        try:
            resident = sess.query(func.count(cls.isResident)).filter(cls.isResident == True).scalar()
        finally:
            sess.close()

        return resident

    @classmethod
    def getUserRate(cls, uid):
        ''' Retrieve the currRate of user with userID, uid.
        '''
        sess = Session()
        try:
            rate = sess.query(cls.currRate).filter(cls.userID == uid).scalar()
        finally:
            sess.close()

        return rate
