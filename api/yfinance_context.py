import yfinance as yf

class YFinanceContext:
    def __init__(self, logger, database):
        self.logger = logger
        self.database = database
        self.logger.log("Initialized YFinanceContext")
        
    def fetch(self, args, attribute):
        sub = getattr(args, attribute)
        self.logger.log(f"Fetching data for ticker: {sub.ticker}")
        try:
            if sub.start is not None and sub.end is not None:
                data = yf.Ticker(sub.ticker).history(start=sub.start, end=sub.end, interval=sub.interval)
            else:
                data = yf.Ticker(sub.ticker).history(period=sub.period, interval=sub.interval)
            self.logger.log(f"Data fetched successfully for ticker: {sub.ticker}")
            return data
        except Exception as e:
            self.logger.log(f"Error fetching data for ticker: {sub.ticker} - {e}")
            
    def download(self, args, attribute):
        self.logger.log(f"Downloading data for stocks: {args.stocks}")
        try:
            if args.start is not None and args.end is not None:
                data = yf.download(args.stocks, start=args.start, end=args.end, interval=args.interval)
            else:
                data = yf.download(args.stocks, period=args.period, interval=args.interval)
            self.logger.log(f"Data downloaded successfully for stocks: {args.stocks}")
            return data
        except Exception as e:
            self.logger.log(f"Error downloading data for ticker: {sub.ticker} - {e}")