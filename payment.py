#!/usr/bin/env python3
'''
Payments class for table models.
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

    @classmethod
    def new_payment(cls):
        ''' Creates and returns a new Payment object representing a payments record.
        '''
        from user import User
        from bill import Bill
        from transaction import Transaction

        # Collect attributes
        uID = input("Enter userID: ")
        bID = input(f"Enter biilID: ")
        tID = input(f"Enter transactionID: ")
        amtPaid = input(f"Enter amoumtPaid: ")

        # Get related parent objects
        sess = Session()
        try:
            usr = sess.query(User).get(int(uID) if len(uID) > 0 else None)
            bil = sess.query(Bill).get(int(bID) if len(bID) > 0 else None)
            trn = sess.query(Transaction).get(int(tID) if len(tID) > 0 else None)

            # Update balance of related bill record
            bil.balance = bil.balance - int(amtPaid)
            sess.add(bil)
            sess.commit()
        finally:
            sess.close()

        # Create object
        payment = cls(
                userID=(int(uID) if len(uID) > 0 else None),
                billID=(int(bID) if len(bID) > 0 else None),
                transactionID=(int(tID) if len(tID) > 0 else None),
                amountPaid=(int(amtPaid) if len(amtPaid) > 0 else None),
                user=usr,
                bill=bil,
                transaction=trn
                )

        return payment

    @classmethod
    def is_completed(cls):
        ''' Check operation flag of model table.
        '''
        from flag import Flag
        sess = Session()

        try:
            # Get flag for users
            qobj = sess.query(Flag.flag).filter(Flag.operation == 'payments')
            flag = qobj.scalar()
            if not flag:
                return True
        except Exception as e:
            raise e
        finally:
            sess.close()

        return False
