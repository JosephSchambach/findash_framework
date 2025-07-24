from pydantic import BaseModel
from typing import Optional, Dict, List

class Stock(BaseModel):
    ticker: str
    start: Optional[str] = None
    end: Optional[str] = None
    period: Optional[str] = None
    interval: Optional[str] = "1d"

class FetchStockData(BaseModel):
    stock: Stock
    
class DownloadStockData(BaseModel):
    stocks: List[str]
    start: Optional[str] = None
    end: Optional[str] = None
    period: Optional[str] = None
    interval: Optional[str] = "1d"