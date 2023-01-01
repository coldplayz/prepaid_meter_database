#!/usr/bin/env python3
'''
Program for interfacing with the b2_prepaid_meter database.
'''

from sqlalchemy import create_engine, func, cast
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import sys
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

Session = sessionmaker(bind=engine)

classes = {
        'users': User, 'appliances': Appliance, 'transactions': Transaction,
        'userAppliances': UserAppliance, 'bills': Bill, 'payments': Payment
        }

def display_flag(operation=None):
    ''' Display all operation flags, or a specific one.
        Args:
            operation (str): string representing the name of a table on which
            an applicable operation is being carried out. Defaults to None.
    '''
    sess = Session()
    try:
        if operation:
            # A specified operation
            qobj = sess.query(Flag.operation, Flag.flag).filter(Flag.operation == operation)
            row = qobj.one()  # get the single record returned

            print('operation\tflag')
            print('=========\t====')
            if len(row.operation) < 8:
                print(f'\n{row.operation}\t\t{row.flag}')
            else:
                print(f'\n{row.operation}\t{row.flag}')
        else:
            # Display all flags
            qobj = sess.query(Flag.operation, Flag.flag)
            rows = qobj.all()

            print('operation\tflag')
            print('=========\t====')
            for row in rows:
                if len(row.operation) < 8:
                    print(f'\n{row.operation}\t\t{row.flag}')
                else:
                    print(f'\n{row.operation}\t{row.flag}')
    except Exception as e:
        raise e
    finally:
        sess.close()


def set_flag(operation, flag):
    ''' Set the boolean flag for a table operation.
        Args:
            operation (str): table operation string
            flag (bool): True or False flag.
    '''
    sess = Session()
    try:
        # Get record to update
        qobj = sess.query(Flag).filter(Flag.operation == operation)
        # Retrieve the one returned object
        rec = qobj.one()
        # Modify returned object
        rec.flag = flag

        sess.add(rec)
        sess.commit()
    except Exception as e:
        raise e
    finally:
        sess.close()


def is_completed(ops=[]):
    ''' Checks completion status flags for multiple operations.
        Args:
            ops (list): a list of operations to check.

        Return:
            bool: True if all operations specified in the list,
            ops, have completed status; False otherwise.
    '''
    completed = False
    for op in ops:
        match op:
            case 'users':
                completed = User.is_completed()
            case 'appliances':
                completed = Appliance.is_completed()
            case 'transactions':
                completed = Transaction.is_completed()
            case 'userAppliances':
                completed = UserAppliance.is_completed()
            case 'bills':
                completed = Bill.is_completed()
            case 'payments':
                completed = Payment.is_completed()
            case _:
                pass
        if not completed:
            return False
    return completed

# Parse command
try:
    cmd = sys.argv[1]
except IndexError:
    # Show commands list.
    with open('cmd_list', 'r', encoding='utf-8') as hlp:
        lines = hlp.readlines()
        print(f'{"".join(["#" for i in range(23)])}\n# Available commands. #\n#######################\n')
        for line in lines:
            print(line)
    sys.exit(0)

match cmd:
    case '-nu':
        # Create new User object
        newUser = User.new_user()
        # Set flag to indicate on-going user-creation operations
        set_flag('users', True)
        # Create database session
        sess = Session()
        try:
            sess.add(newUser)
            sess.commit()
        except Exception as e:
            raise e
        finally:
            sess.close()
    case '-uc':
        # Set flag to indicate completion of insertion operations on users table.
        set_flag('users', False)
    case '-cr':
        # [Re]compute rates
        if is_completed(['users', 'appliances', 'transactions', 'userAppliances']):
            User.calc_rates()
        else:
            print('Check for completion of users, appliances, transactions, and/or userAppliances operations, and try again.')
    case '-na':
        # Add new appliance
        newAppliance = Appliance.new_appliance()
        set_flag('appliances', True)
        sess = Session()
        try:
            sess.add(newAppliance)
            sess.commit()
        except Exception as e:
            raise e
        finally:
            sess.close()
    case '-ac':
        set_flag('appliances', False)
    case '-nt':
        # Add new transaction
        newTransaction = Transaction.new_transaction()
        set_flag('transactions', True)
        sess = Session()
        try:
            sess.add(newTransaction)
            sess.commit()
        except Exception as e:
            raise e
        finally:
            sess.close()
    case '-tc':
        set_flag('transactions', False)
    case '-nua':
        # Ensure there is no pending users, appliances, or transactions operation.
        if not User.is_completed:
            print('Complete users operation and try again.')
            sys.exit(1)
        if not Appliance.is_completed:
            print('Complete appliances operation and try again.')
            sys.exit(1)
        if not Transaction.is_completed:
            print('Complete transactions operation and try again.')
            sys.exit(1)
        # Add new userAppliance record
        newUserAppliance = UserAppliance.new_userAppliance()
        set_flag('userAppliances', True)
        sess = Session()
        try:
            sess.add(newUserAppliance)
            sess.commit()
        except Exception as e:
            raise e
        finally:
            sess.close()
    case '-uac':
        set_flag('userAppliances', False)
    case '-df':
        # Display flag(s)
        try:
            op = sys.argv[2]
        except IndexError:
            op = None

        display_flag(operation=op)
    case '-sf':
        ''' Flag-setting is meant to be an
        internal logic, and not to have an external
        interface. This interface is meant for testing purposes.
        '''
        op = sys.argv[2]
        flag = True if sys.argv[3] == 'True' else False
        set_flag(op, flag)
    case '-cf':
        # Test check for table operation flag value
        print(classes[sys.argv[2]].is_completed())
    case _:
        pass
