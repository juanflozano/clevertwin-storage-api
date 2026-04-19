from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database import SessionLocal
from models import StorageEvent
from schemas import Event
from auth import verify_token

router = APIRouter()
security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_company(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    company = verify_token(token)
    if company is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return company

@router.get("/events")
def get_events(db: Session = Depends(get_db), current_company: str = Depends(get_current_company)):
    events = db.query(StorageEvent).filter(StorageEvent.company == current_company).all()
    return events

@router.get("/events/{company}")
def get_events_by_company(company: str, db: Session = Depends(get_db), current_company: str = Depends(get_current_company)):
    events = db.query(StorageEvent).filter(StorageEvent.company == company).all()
    if not events:
        raise HTTPException(status_code=404, detail="Company not found")
    return events

@router.post("/events")
def create_event(event: Event, db: Session = Depends(get_db), current_company: str = Depends(get_current_company)):
    db_event = StorageEvent(
        company=event.company,
        event_type=event.event_type,
        file_size=event.file_size,
        file_type=event.file_type
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.delete("/events/{id}")
def delete_event(id: int, db: Session = Depends(get_db), current_company: str = Depends(get_current_company)):
    event = db.query(StorageEvent).filter(StorageEvent.id == id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Id not found in events")
    db.delete(event)
    db.commit()
    return {"message": f"Event with id: '{id}' deleted successfully"}

@router.put("/events/{id}")
def update_event(id: int, event: Event, db: Session = Depends(get_db), current_company: str = Depends(get_current_company)):
    event_found = db.query(StorageEvent).filter(StorageEvent.id == id).first()
    if not event_found:
        raise HTTPException(status_code=404, detail="Id not found in events")
    event_found.company = event.company
    event_found.event_type = event.event_type
    event_found.file_size = event.file_size
    event_found.file_type = event.file_type
    db.commit()
    db.refresh(event_found)
    return {"message": f"Event with '{id}' id was successfully updated to {event_found}"}