from pydantic import BaseModel
from typing import Optional, Dict, List

class Asset(BaseModel):
    ticker: str
    start: Optional[str] = None
    end: Optional[str] = None
    period: Optional[str] = None
    interval: Optional[str] = "1d"

class FetchAssetData(BaseModel):
    asset: Asset

class DownloadAssetData(BaseModel):
    assets: List[str]
    start: Optional[str] = None
    end: Optional[str] = None
    period: Optional[str] = None
    interval: Optional[str] = "1d"