from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NetFaultLabBase(BaseModel):
    source: str
    severity: str
    description: str
    affected_services: str

class NetFaultLabCreate(NetFaultLabBase):
    pass

class NetFaultLabRead(NetFaultLabBase):
    id: str
    timestamp: datetime
    resolved: bool

class NetFaultLabList(BaseModel):
    items: list[NetFaultLabRead]

class NetFaultLabAnalytics(BaseModel):
    total_incidents: int
    resolved_incidents: int
    unresolved_incidents: int
    severity_breakdown: dict[str, int]
    average_response_time: float