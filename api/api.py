from api.api_obj_config import api_obj_config
from api.yfinance_context import YFinanceContext
from api.databricks import DataBricksContext
from findash_utilities import get_secret
import pandas as pd

class API:
    def __init__(self, logger, database):
        self.logger = logger
        self.database = database
        self._yfinance = YFinanceContext(logger=self.logger, database=self.database)
        self._databricks = self._databricks_api()
        self.obj_config = api_obj_config(self)
        self.logger.log("Initialized API context")
        
    def _databricks_api(self):
        databricks_tokens = get_secret("databricks_tokens")
        if not databricks_tokens:
            self.logger.log("Failed to retrieve Databricks tokens from secrets manager.")
            raise Exception("Databricks tokens not found.")
        __token = databricks_tokens.get("DATABRICKS_TOKEN")
        __endpoint = databricks_tokens.get("DATABRICKS_ENDPOINT")
        return DataBricksContext(
            token=__token,
            endpoint=__endpoint,
            logger=self.logger,
            database=self.database
        )

    def fetch(self, args, log=True, alert=True):
        arg_type = type(args)
        fetch_response = []
        if log:
            self.logger.log(f"Fetching data {arg_type.__name__}")
        if not isinstance(args, list):
            args = [args]
        for i, arg in enumerate(args):
            self.logger.log(f"Fetching data {i+1}: {arg_type.__name__}")
            kwargs = self.obj_config[arg.__class__.__name__]
            if not kwargs:
                self.logger.log(f"No configuration found for {arg.__class__.__name__}")
                continue
            result = self._execute(arg, kwargs, alert)
            fetch_response.append(result)
        if len(fetch_response) == 1:
            return fetch_response[0]
        return fetch_response
    
    def send(self, args, log=True, alert=True):
        arg_type = type(args)
        send_response = []
        if log:
            self.logger.log(f"Sending data {arg_type.__name__}")
        if not isinstance(args, list):
            args = [args]
        for i, arg in enumerate(args):
            self.logger.log(f"Sending data {i+1}: {arg_type.__name__}")
            kwargs = self.obj_config[arg.__class__.__name__]
            if not kwargs:
                self.logger.log(f"No configuration found for {arg.__class__.__name__}")
                continue
            result = self._execute(arg, kwargs, alert)
            send_response.append(result)
        if len(send_response) == 1:
            return send_response[0]
        return send_response
            
    def _execute(self, args, kwargs, alert, log=True, retries=0):
        parent_method = kwargs.get("parent_method")
        kwargs = kwargs.get("kwargs", {})
        attribute = kwargs.get("attribute")
        if log:
            self.logger.log(f"Processing {attribute}")
        for retry in range(retries + 1):
            try:
                if kwargs == {}:
                    return parent_method(args)
                else:
                    return parent_method(args, **kwargs)
            except Exception as e:
                if retry < retries:
                    self.logger.log(f"Retry {retry + 1} for {attribute} failed: {e}")
                else:
                    self.logger.log(f"All retries for {attribute} failed: {e}")
                    if alert:
                        pass  # Handle alert logic here
        return None