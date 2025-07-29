from models.authorization_models import ValidateUser, RegisterUser
from pydantic import EmailStr
import base64 as b64

class AuthorizationContext:
    def __init__(self, database, logger):
        self.database = database
        self.logger = logger
        self.logger.log("Initialized AuthorizationContext")

    def validate(self, args, log=False):
        if isinstance(args, ValidateUser):
            self.__password = b64.b64decode(args.password.encode()).decode()
            data = self.database.pandas_select(
                "select id from user where username = %s and password = %s",
                (args.username, self.__password)
            )
            if not data.empty:
                self.logger.log(f"User validated successfully.")
                self._user_id = data.iloc[0]['id']
                self._username = args.username
                self._password = args.password
                return 'User validated successfully.'
            else:
                self.logger.log(f"User validation failed.")
                return 'User validation failed.'
        else:
            self.logger.log("Invalid arguments for validation")
            raise ValueError("Invalid arguments for validation")
    
    def register(self, args, log=False):
        if isinstance(args, RegisterUser):
            self.logger.log(f"Registering user")
            if self._check_for_username(args.username):
                self.logger.log(f"Username already exists.")
                return False
            self.__password = args.password
            self.__username = args.username
            self.__email = args.email
            self.__phone = args.phone
            if not self._validate_phone(self.__phone):
                self.logger.log(f"Invalid phone number.")
                return 'Invalid phone number.'
            if not self._validate_email(self.__email):
                self.logger.log(f"Invalid email address.")
                return 'Invalid email address.'
            data = self.database.execute(
                "insert into user (username, password, email, phone) values (%s, %s, %s, %s)",
                (self.__username, self.__password, self.__email, self.__phone)
            )
            return 'User registered successfully.'
        else:
            self.logger.log("Invalid arguments for registration")
            raise ValueError("Invalid arguments for registration")
        
    def _check_for_username(self, username):
        data = self.database.pandas_select(
            "select id from user where username = %s",
            (username,)
        )
        return not data.empty

    def _validate_email(self, email):
        try:
            EmailStr.validate(email)
            return True
        except ValueError:
            return False

    def _validate_phone(self, phone):
        if len(phone) != 10 or not phone.isdigit():
            return False
        return True