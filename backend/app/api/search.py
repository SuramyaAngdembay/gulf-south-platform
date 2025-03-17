from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Research, Event, Resource
from app.schemas.search import SearchResult
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/search", response_model=List[SearchResult])
async def global_search(
    q: str = Query(..., description="Search query"),
    type: Optional[str] = Query(None, description="Content type filter"),
    era: Optional[List[str]] = Query(None, description="Era filters"),
    date_range: Optional[List[datetime]] = Query(None, description="Date range filter"),
    resource_type: Optional[List[str]] = Query(None, description="Resource type filter"),
    status: Optional[List[str]] = Query(None, description="Status filter"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Global search across all content types with advanced filtering
    """
    results = []
    
    # Base query conditions
    base_conditions = []
    if era:
        base_conditions.append(Research.era.in_(era))
    if date_range and len(date_range) == 2:
        base_conditions.append(Research.start_date.between(date_range[0], date_range[1]))
    if status:
        base_conditions.append(Research.status.in_(status))

    # Search in research projects
    if not type or type == "research":
        research_query = db.query(Research).filter(
            Research.title.ilike(f"%{q}%") | Research.description.ilike(f"%{q}%")
        )
        for condition in base_conditions:
            research_query = research_query.filter(condition)
        
        for research in research_query.all():
            results.append(SearchResult(
                id=research.id,
                type="research",
                title=research.title,
                description=research.description,
                date=research.start_date,
                metadata={
                    "era": research.era,
                    "status": research.status,
                    "lead_researcher": research.lead_researcher.name
                }
            ))

    # Search in events
    if not type or type == "events":
        event_query = db.query(Event).filter(
            Event.title.ilike(f"%{q}%") | Event.description.ilike(f"%{q}%")
        )
        if date_range and len(date_range) == 2:
            event_query = event_query.filter(Event.date.between(date_range[0], date_range[1]))
        if status:
            event_query = event_query.filter(Event.status.in_(status))
        
        for event in event_query.all():
            results.append(SearchResult(
                id=event.id,
                type="event",
                title=event.title,
                description=event.description,
                date=event.date,
                metadata={
                    "type": event.type,
                    "status": event.status,
                    "location": event.location
                }
            ))

    # Search in resources
    if not type or type == "resources":
        resource_query = db.query(Resource).filter(
            Resource.title.ilike(f"%{q}%") | Resource.description.ilike(f"%{q}%")
        )
        if resource_type:
            resource_query = resource_query.filter(Resource.type.in_(resource_type))
        if date_range and len(date_range) == 2:
            resource_query = resource_query.filter(Resource.created_at.between(date_range[0], date_range[1]))
        
        for resource in resource_query.all():
            results.append(SearchResult(
                id=resource.id,
                type=resource.type,
                title=resource.title,
                description=resource.description,
                date=resource.created_at,
                metadata={
                    "type": resource.type,
                    "format": resource.format,
                    "author": resource.author.name
                }
            ))

    # Sort results by date
    results.sort(key=lambda x: x.date, reverse=True)
    
    return results 