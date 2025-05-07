from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from database.db import SessionLocal
from models.schema import Referral, EmailStatusEnum, ResponseStatusEnum

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create one
@router.post("/")
def create_referral(payload: dict, db: Session = Depends(get_db)):
    item = Referral(**payload)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# List all with filters + pagination + sorting
@router.get("/")
def list_referrals(
    job_id: int = Query(None),
    user_id: int = Query(None),
    email_status: EmailStatusEnum = Query(None),
    response_status: ResponseStatusEnum = Query(None),
    critical: int = Query(None, ge=0, le=5),
    sort_by: str = Query("timestamp"),
    order: str = Query("desc"),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(Referral)

    if job_id:
        query = query.filter(Referral.job_id == job_id)
    if user_id:
        query = query.filter(Referral.user_id == user_id)
    if email_status:
        query = query.filter(Referral.email_status == email_status)
    if response_status:
        query = query.filter(Referral.response_status == response_status)
    if critical is not None:
        query = query.filter(Referral.critical == critical)

    # Apply sorting
    if hasattr(Referral, sort_by):
        order_by = desc(getattr(Referral, sort_by)) if order == "desc" else asc(getattr(Referral, sort_by))
        query = query.order_by(order_by)

    total = query.count()
    results = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "results": results
    }

# Read one
@router.get("/{referral_id}")
def read_one(referral_id: int, db: Session = Depends(get_db)):
    item = db.query(Referral).filter(Referral.id == referral_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Referral not found")
    return item

# Update one
@router.put("/{referral_id}")
def update_one(referral_id: int, updates: dict, db: Session = Depends(get_db)):
    item = db.query(Referral).filter(Referral.id == referral_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Referral not found")
    for key, value in updates.items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

# Update multiple
@router.put("/")
def update_multiple(updates: list[dict], db: Session = Depends(get_db)):
    updated = []
    for entry in updates:
        item = db.query(Referral).filter(Referral.id == entry["id"]).first()
        if item:
            for key, value in entry.items():
                if key != "id":
                    setattr(item, key, value)
            updated.append(item)
    db.commit()
    return updated

# Delete one
@router.delete("/{referral_id}")
def delete_one(referral_id: int, db: Session = Depends(get_db)):
    item = db.query(Referral).filter(Referral.id == referral_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Referral not found")
    db.delete(item)
    db.commit()
    return { "message": "Referral deleted successfully." }

# Delete multiple
@router.delete("/")
def delete_multiple(ids: list[int], db: Session = Depends(get_db)):
    db.query(Referral).filter(Referral.id.in_(ids)).delete(synchronize_session=False)
    db.commit()
    return { "message": "Multiple referrals deleted successfully." }
