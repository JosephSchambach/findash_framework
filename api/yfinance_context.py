import yfinance as yf

class YFinanceContext:
    def __init__(self, logger, database):
        self.logger = logger
        self.database = database
        self.logger.log("Initialized YFinanceContext")
        
    def fetch(self, args, attribute):
        sub = getattr(args, attribute)
        self.logger.log(f"Fetching data for asset: {sub.asset}")
        try:
            if sub.start is not None and sub.end is not None:
                data = yf.Ticker(sub.asset).history(start=sub.start, end=sub.end, interval=sub.interval)
            else:
                data = yf.Ticker(sub.asset).history(period=sub.period, interval=sub.interval)
            self.logger.log(f"Data fetched successfully for asset: {sub.asset}")
            return data
        except Exception as e:
            self.logger.log(f"Error fetching data for asset: {sub.asset} - {e}")

    def download(self, args, attribute):
        self.logger.log(f"Downloading data for assets: {args.assets}")
        try:
            if args.start is not None and args.end is not None:
                data = yf.download(args.assets, start=args.start, end=args.end, interval=args.interval)
            else:
                data = yf.download(args.assets, period=args.period, interval=args.interval)
            self.logger.log(f"Data downloaded successfully for assets: {args.assets}")
            return data
        except Exception as e:
            self.logger.log(f"Error downloading data for assets: {args.assets} - {e}")