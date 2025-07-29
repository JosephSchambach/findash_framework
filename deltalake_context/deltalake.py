from deltalake_context.etl_config import etl_config

class Deltalake:
    def __init__(self, s3_context, sql_context, logger):
        self.s3_context = s3_context
        self.sql_context = sql_context
        self.logger = logger
        self.etl_config = etl_config()
        self.logger.log("Deltalake context initialized.")
        
    def etl(self, data, table_name):
        ''' Perform ETL operations on the data and write to Delta Lake '''
        pass
    
    def query(self, query):
        ''' Execute a query on the Delta Lake '''
        pass