from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..schemas.netfaultlab import NetFaultLabCreate, NetFaultLabRead, NetFaultLabList, NetFaultLabAnalytics
from ..services.netfaultlab_service import NetFaultLabService
from ..core.db import get_db
import aiosqlite

router = APIRouter()

@router.post("/", response_model=NetFaultLabRead, status_code=201)
async def create_incident(
    incident: NetFaultLabCreate,
    service: NetFaultLabService = Depends()
):
    return await service.create_incident(incident)

@router.get("/", response_model=NetFaultLabList)
async def list_incidents(
    service: NetFaultLabService = Depends()
):
    return await service.list_incidents()

@router.get("/{incident_id}", response_model=NetFaultLabRead)
async def get_incident(
    incident_id: str,
    service: NetFaultLabService = Depends()
):
    return await service.get_incident(incident_id)

@router.get("/analytics", response_model=NetFaultLabAnalytics)
async def get_analytics(
    service: NetFaultLabService = Depends()
):
    return await service.get_analytics()