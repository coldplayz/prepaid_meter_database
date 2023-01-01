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
        if isRsdnt:
            # Non-empty string
            isRsdnt = True if isRsdnt == 'True' else False
        else:
            isRsdnt = None

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
