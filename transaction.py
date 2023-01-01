#!/usr/bin/env python3
'''
Transaction class for table models.
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

class Transaction(Base):
    # Define table name
    __tablename__ = 'transactions'

    ''' Define column-attributes.
        Format:
            col_name = Column(data_type, ...)
    '''
    transactionID = Column(Integer, primary_key=True)
    transactionAmt = Column(Integer, nullable=False)
    totalOldDebt = Column(Integer, nullable=False)
    totalNetRecharge = Column(Integer, Computed('transactionAmt - totalOldDebt', persisted=True))
    created_on = Column(Date, default=datetime.now().date)

    # Relationships
    transactionBills = relationship("Bill", backref='transaction', cascade="all, delete-orphan")
    transactionUserAppliances = relationship("UserAppliance", backref='transaction', cascade="all, delete-orphan")
    transactionPayments = relationship("Payment", backref='transaction', cascade="all, delete-orphan")

    ''' Define table-level constraints.
        Format:
            __table_args__ = (comma-separated list of table constraints)
    '''
    # Code here

    @classmethod
    def new_transaction(cls):
        ''' Creates and returns a new Transaction object representing a transactions record.
        '''

        # Collect attributes
        tAmount = input("Enter transactionAmt: ")
        totOldDebt = input(f"Enter total old debt: ")

        # Create object
        transaction = cls(
                transactionAmt=(int(tAmount) if len(tAmount) > 0 else None),
                totalOldDebt=(int(totOldDebt) if len(totOldDebt) > 0 else None)
                )

        return transaction

    @classmethod
    def is_completed(cls):
        ''' Check operation flag of model table.
        '''
        from flag import Flag
        sess = Session()

        try:
            # Get flag for transactions
            qobj = sess.query(Flag.flag).filter(Flag.operation == 'transactions')
            flag = qobj.scalar()
            if not flag:
                return True
        except Exception as e:
            raise e
        finally:
            sess.close()

        return False

    @classmethod
    def latest_transaction_rec(cls):
        ''' Fetch the most recent transaction record.
        '''
        sess = Session()
        try:
            # Get max transactionID
            maxID = sess.query(func.max(Transaction.transactionID)).scalar()

            # Get the required record
            latest = sess.query(Transaction).filter(Transaction.transactionID == maxID).one()
        finally:
            sess.close()

        return latest
