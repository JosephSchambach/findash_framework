from models.authorization_models import ValidateUser, RegisterUser
import base64 as b64

class AuthorizationContext:
    def __init__(self, database, logger):
        self.database = database
        self.logger = logger
        self.logger.log("Initialized AuthorizationContext")

    def validate(self, args, log=False):
        if isinstance(args, ValidateUser):
            self.logger.log(f"Validating user: {args.username}")
            self.__password = b64.b64decode(args.password.encode()).decode()
            data = self.database.pandas_select(
                "select id from user where username = %s and password = %s",
                (args.username, self.__password)
            )
            if not data.empty:
                self.logger.log(f"User {args.username} validated successfully.")
                self._user_id = data.iloc[0]['id']
                self._username = args.username
                self._password = args.password
                return True
            else:
                self.logger.log(f"User {args.username} validation failed.")
                return False
        else:
            self.logger.log("Invalid arguments for validation")
            raise ValueError("Invalid arguments for validation")
    
    def register(self, args, log=False):
        if isinstance(args, RegisterUser):
            self.logger.log(f"Registering user: {args.username}")
            if self._check_for_username(args.username):
                self.logger.log(f"Username {args.username} already exists.")
                return False
            self.__password = args.password
            self.__username = args.username
            self.__email = args.email
            self.__phone = args.phone
            data = self.database.execute(
                "insert into user (username, password, email, phone) values (%s, %s, %s, %s)",
                (self.__username, self.__password, self.__email, self.__phone)
            )
            return True
        else:
            self.logger.log("Invalid arguments for registration")
            raise ValueError("Invalid arguments for registration")
        
    def _check_for_username(self, username):
        data = self.database.pandas_select(
            "select id from user where username = %s",
            (username,)
        )
        return not data.empty