import aiosqlite
from typing import List
from ..schemas.netfaultlab import NetFaultLabCreate, NetFaultLabRead
from ..core.db import get_db
from uuid import uuid4
from datetime import datetime
import json

async def get_db_connection():
    """Get a database connection."""
    async for conn in get_db():
        return conn

async def create_incident(incident: NetFaultLabCreate) -> NetFaultLabRead:
    """Create a new incident."""
    incident_id = str(uuid4())
    timestamp = datetime.utcnow().isoformat()
    
    async with await get_db_connection() as conn:
        await conn.execute(
            "INSERT INTO incidents (id, timestamp, source, severity, description, resolved, affected_services) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (incident_id, timestamp, incident.source, incident.severity, incident.description, False, incident.affected_services)
        )
        await conn.commit()
    
    return NetFaultLabRead(
        id=incident_id,
        timestamp=datetime.fromisoformat(timestamp),
        source=incident.source,
        severity=incident.severity,
        description=incident.description,
        resolved=False,
        affected_services=incident.affected_services
    )

async def list_incidents() -> List[NetFaultLabRead]:
    """List all incidents."""
    async with await get_db_connection() as conn:
        cursor = await conn.execute("SELECT id, timestamp, source, severity, description, resolved, affected_services FROM incidents")
        rows = await cursor.fetchall()
    
    incidents = []
    for row in rows:
        incidents.append(NetFaultLabRead(
            id=row[0],
            timestamp=datetime.fromisoformat(row[1]),
            source=row[2],
            severity=row[3],
            description=row[4],
            resolved=row[5],
            affected_services=row[6]
        ))
    
    return incidents

async def get_incident(incident_id: str) -> NetFaultLabRead:
    """Get a specific incident by ID."""
    async with await get_db_connection() as conn:
        cursor = await conn.execute(
            "SELECT id, timestamp, source, severity, description, resolved, affected_services FROM incidents WHERE id = ?",
            (incident_id,)
        )
        row = await cursor.fetchone()
    
    if not row:
        raise ValueError(f"Incident {incident_id} not found")
    
    return NetFaultLabRead(
        id=row[0],
        timestamp=datetime.fromisoformat(row[1]),
        source=row[2],
        severity=row[3],
        description=row[4],
        resolved=row[5],
        affected_services=row[6]
    )

async def get_analytics():
    """Get analytics data for incidents."""
    from typing import Dict
    
    async with await get_db_connection() as conn:
        cursor = await conn.execute("SELECT COUNT(*) FROM incidents")
        total_incidents = (await cursor.fetchone())[0]
        
        cursor = await conn.execute("SELECT COUNT(*) FROM incidents WHERE resolved = 1")
        resolved_incidents = (await cursor.fetchone())[0]
        
        cursor = await conn.execute("SELECT COUNT(*) FROM incidents WHERE resolved = 0")
        unresolved_incidents = (await cursor.fetchone())[0]
        
        cursor = await conn.execute("SELECT severity, COUNT(*) FROM incidents GROUP BY severity")
        severity_rows = await cursor.fetchall()
        severity_breakdown = {row[0]: row[1] for row in severity_rows}
        
        cursor = await conn.execute("SELECT AVG(strftime('%s', timestamp)) FROM incidents")
        avg_timestamp = (await cursor.fetchone())[0]
        average_response_time = avg_timestamp if avg_timestamp else 0.0
    
    return {
        "total_incidents": total_incidents,
        "resolved_incidents": resolved_incidents,
        "unresolved_incidents": unresolved_incidents,
        "severity_breakdown": severity_breakdown,
        "average_response_time": average_response_time
    }