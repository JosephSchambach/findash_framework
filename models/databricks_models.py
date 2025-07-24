from pydantic import BaseModel
from typing import Optional, Dict, List

class DatabricksJob(BaseModel):
    job_id: int
    
class SendDataBricksJob(BaseModel):
    job: DatabricksJob