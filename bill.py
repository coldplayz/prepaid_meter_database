#!/usr/bin/env python3
'''
user bills class for table models.
'''

from sqlalchemy import Computed, create_engine, Column, Integer, SmallInteger, String, Boolean, Date, Numeric, ForeignKey, func, cast, ForeignKeyConstraint, CheckConstraint
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from decimal import Decimal
# from sqlalchemy.ext.declarative import declarative_base
from user import Base

engine = create_engine(
        'mysql+mysqldb://Bel2:PASSWORD@localhost/b2_prepaid_meter',
        pool_pre_ping=True)

Session = sessionmaker(bind=engine)

class Bill(Base):
    # Define table name
    __tablename__ = 'bills'

    ''' Define column-attributes.
        Format:
            col_name = Column(data_type, ...)
    '''
    billID = Column(Integer, primary_key=True)
    userID = Column(Integer, ForeignKey('users.userID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    transactionID = Column(Integer, ForeignKey('transactions.transactionID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    oldDebtShare = Column(Numeric(10, 2), nullable=False)
    netRechargeShare = Column(Numeric(10, 2), nullable=False)
    amountDue = Column(Integer, Computed('CAST((oldDebtShare + netRechargeShare) AS SIGNED)', persisted=True))
    dueDate = Column(Date, default=datetime.now().date)
    balance = Column(Integer, default=amountDue)

    # Relationships
    billPayments = relationship("Payment", backref='bill', cascade="all, delete-orphan")

    ''' Define table-level constraints.
        Format:
            __table_args__ = (comma-separated list of table constraints)
    '''
    __table_args__ = (CheckConstraint('balance >= 0', name='check_balance'),)

    @classmethod
    def new_bill(cls):
        ''' Creates and returns a new Bill object representing a bills record.
        '''
        from user import User
        from transaction import Transaction

        # Collect attributes
        uID = input("Enter userID: ")
        tID = input(f"Enter transactionID: ")

        # Get latest transaction record
        latestTransaction = Transaction.latest_transaction_rec()
        # Get number of active users
        residentUsers = User.residentUsers()
        # Get user rate
        rate = User.getUserRate(int(uID))
        # Calculate payment shares
        odShare = Decimal(latestTransaction.totalOldDebt / residentUsers)
        nrShare = Decimal(latestTransaction.totalNetRecharge * rate)

        # Get related parent objects
        sess = Session()
        try:
            usr = sess.query(User).get(int(uID) if len(uID) > 0 else None)
            trn = sess.query(Transaction).get(int(tID) if len(tID) > 0 else None)
        finally:
            sess.close()

        # Create object
        bill = cls(
                userID=(int(uID) if len(uID) > 0 else None),
                transactionID=(int(tID) if len(tID) > 0 else None),
                oldDebtShare=odShare,
                netRechargeShare=nrShare,
                balance=cast(odShare + nrShare, Integer),
                user=usr,
                transaction=trn
                )

        return bill

    @classmethod
    def is_completed(cls):
        ''' Check operation flag of model table.
        '''
        from flag import Flag
        sess = Session()

        try:
            # Get flag for users
            qobj = sess.query(Flag.flag).filter(Flag.operation == 'bills')
            flag = qobj.scalar()
            if not flag:
                return True
        except Exception as e:
            raise e
        finally:
            sess.close()

        return False
