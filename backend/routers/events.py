from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from models import StorageEvent
from schemas import Event
from datetime import datetime
from dependencies import get_db, get_current_company
import boto3
import json

router = APIRouter()
security = HTTPBearer()

def save_log_to_s3(event_type: str, company: str, event_data: dict):
    try:
        s3 = boto3.client("s3", region_name="us-east-1")
        
        log = {
            "event_type": event_type,
            "company": company,
            "timestamp": datetime.utcnow().isoformat(),
            "data": event_data
        }
        
        key = f"logs/{company}/{event_type}/{datetime.utcnow().strftime('%Y/%m/%d')}/{datetime.utcnow().isoformat()}.json"
        
        s3.put_object(
            Bucket="clevertwin-storage-logs",
            Key=key,
            Body=json.dumps(log),
            ContentType="application/json"
        )
        print(f"[LOG] Saved to S3: {key}")
    except Exception as e:
        print(f"[LOG] Error saving log: {e}")

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

    save_log_to_s3("upload", current_company, {
        "id": db_event.id,
        "company": db_event.company,
        "event_type": db_event.event_type,
        "file_size": db_event.file_size,
        "file_type": db_event.file_type
    })

    return db_event
   
@router.delete("/events/{id}")
def delete_event(id: int, db: Session = Depends(get_db), current_company: str = Depends(get_current_company)):
    event = db.query(StorageEvent).filter(StorageEvent.id == id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Id not found in events")
    event_data = {
        "id": event.id,
        "company": event.company,
        "event_type": event.event_type,
        "file_size": event.file_size,
        "file_type": event.file_type
    }
    db.delete(event)
    db.commit()
    save_log_to_s3("delete", current_company, event_data)
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

@router.get("/stats")
def get_stats(db: Session = Depends(get_db), current_company: str = Depends(get_current_company)):
    events = db.query(StorageEvent).filter(StorageEvent.company == current_company).all()
    stats = {
        "company": current_company,
        "total_uploads_mb": sum(e.file_size for e in events if e.event_type == "upload"),
        "total_downloads_mb": sum(e.file_size for e in events if e.event_type == "download"),
        "total_deletes_mb": sum(e.file_size for e in events if e.event_type == "delete"),
        "total_events": len(events)
    }
    return stats