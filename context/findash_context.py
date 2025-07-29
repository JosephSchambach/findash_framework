import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from context.logger import FinDashLogger
from sub_context.sql_context import SQLContext
from sub_context.s3_context import S3Context
from authorization.authorization_context import AuthorizationContext
from api.api import API
from dotenv import load_dotenv
from findash_utilities import get_secret

load_dotenv()

class FinDashContext:
    def __init__(self):
        self.logger = FinDashLogger()
        self.logger.log("Initializing FinDashContext")
        self.__validate_user()
        self._get_sql_context()
        self._get_s3_context()
        self._get_api_context()
        self._get_authorization()

    def __validate_user(self):
        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")
        
        user_credentials = get_secret("user_creds")
        if not user_credentials:
            self.logger.log("Failed to retrieve user credentials from secrets manager.")
            raise Exception("User credentials not found.")
        if username in user_credentials.keys() and user_credentials[username] == password:
            self.logger.log(f"User {username} validated successfully.")
            self._username = username
            self._password = password
        else:
            self.logger.log(f"User {username} validation failed.")
            raise Exception("Invalid username or password.")
        
    def _get_authorization(self):
        self.authorization = AuthorizationContext(database=self.sql_context, logger=self.logger)
        
    def _get_sql_context(self):
        sql_tokens = os.getenv("SQL_TOKENS")
        sql_context = get_secret(sql_tokens)
        if not sql_context:
            self.logger.log("Failed to retrieve SQL context from secrets manager.")
            raise Exception("SQL context not found.")
        host = sql_context.get("host")
        port = sql_context.get("port")
        user = sql_context.get("username")
        password = sql_context.get("password")
        database = sql_context.get("database")
        self.sql_context = SQLContext(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            logger=self.logger
        )
        
    def _get_s3_context(self):
        access_key = os.getenv("AWS_ACCESS_KEY")
        secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        region = os.getenv("AWS_REGION")
        if not access_key or not secret_key or not region:
            self.logger.log("AWS credentials are not set in the environment variables.")
            raise Exception("AWS credentials not found.")
        self.s3_context = S3Context(
            access_key=access_key,
            secret_key=secret_key,
            region=region,
            logger=self.logger
        )

    def _get_api_context(self):
        self.api = API(logger=self.logger, database=self.sql_context)
