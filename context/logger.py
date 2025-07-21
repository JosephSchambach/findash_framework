import logging

class FinDashLogger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        handler = logging.FileHandler('findash.log', mode='a')
        formatter = logging.Formatter('%(asctime)s - findash - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        
    def log(self, message):
        print(message)
        self.logger.info(message)