#!/usr/bin/env python3
'''
Template class for table models.
'''

from sqlalchemy import Computed, create_engine, Column, Integer, SmallInteger, String, Boolean, DateTime, Numeric, ForeignKey, func, cast, ForeignKeyConstraint, CheckConstraint
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from decimal import Decimal
# from sqlalchemy.ext.declarative import declarative_base
from user import Base

engine = create_engine(
        'mysql+mysqldb://Bel2:44384439@localhost/b2_prepaid_meter',
        pool_pre_ping=True)

Session = sessionmaker(bind=engine)

class Appliance(Base):
    # Define table name
    __tablename__ = 'appliances'

    ''' Define column-attributes.
        Format:
            col_name = Column(data_type, ...)
    '''
    applianceID = Column(Integer, primary_key=True)
    applianceName = Column(String(50), nullable=False)
    wattage = Column(SmallInteger, nullable=False)
    absCost = Column(Numeric(5, 2), nullable=False)
    relCost = Column(Numeric(5, 2), nullable=False)
    adjRelCost = Column(Numeric(5, 2), nullable=False)

    # Relationships
    appliance_users = relationship("UserAppliance", backref='appliance', cascade="all, delete-orphan")

    ''' Define table-level constraints.
        Format:
            __table_args__ = (comma-separated list of table constraints)
    '''
    # Code here

    @classmethod
    def new_appliance(cls):
        ''' Creates and returns a new Appliance object representing an appliances record.
        '''

        # Collect attributes
        appname = input("Enter applianceName: ")
        watt = input(f"Enter {appname if len(appname) > 0 else 'applianceName'}'s wattage: ")
        aCost = input(f"Enter {appname if len(appname) > 0 else 'applianceName'}'s absCost: ")
        rCost = input(f"Enter {appname if len(appname) > 0 else 'applianceName'}'s relCost: ")
        arCost = input(f"Enter {appname if len(appname) > 0 else 'applianceName'}'s adjRelCost: ")

        # Create object
        appliance = cls(
                applianceName=(appname if len(appname) > 0 else None),
                wattage=(int(watt) if len(watt) > 0 else None),
                absCost=(Decimal(aCost) if len(aCost) > 0 else None),
                relCost=(Decimal(rCost) if len(rCost) > 0 else None),
                adjRelCost=(Decimal(arCost) if len(arCost) > 0 else None)
                )

        return appliance

    @classmethod
    def is_completed(cls):
        ''' Check operation flag of model table.
        '''
        from flag import Flag
        sess = Session()

        try:
            # Get flag for users
            qobj = sess.query(Flag.flag).filter(Flag.operation == 'appliances')
            flag = qobj.scalar()
            if not flag:
                return True
        except Exception as e:
            raise e
        finally:
            sess.close()

        return False
