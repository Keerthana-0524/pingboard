from pydantic import BaseModel,Field,HttpUrl
class MonitorBase(BaseModel):
    name:str=Field(min_length=1,max_length=100)
    url: HttpUrl
    interval_seconds: int=Field(default=300,ge=30,le=86400)
    expected_status:int= Field(default=200,ge=100,le=599)

class MonitorCreate(MonitorBase):
    """What client sends"""

class MonitorOut(MonitorBase):
    """What server returns"""
    id:int