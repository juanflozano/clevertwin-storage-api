from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import SessionLocal
from auth import verify_token

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