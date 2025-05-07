from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from database.db import SessionLocal
from models import schema

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create one
@router.post("/")
def create_company(payload: dict, db: Session = Depends(get_db)):
    item = schema.Company(**payload)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# Read all with filter and pagination
@router.get("/")
def list_companies(
    name: str = Query(None),
    domain: str = Query(None),
    email_pattern: str = Query(None),
    is_verified: int = Query(None, ge=0, le=1),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(schema.Company)

    if name:
        query = query.filter(schema.Company.name.ilike(f"%{name}%"))
    if domain:
        query = query.filter(schema.Company.domain.ilike(f"%{domain}%"))
    if email_pattern:
        query = query.filter(schema.Company.email_pattern.ilike(f"%{email_pattern}%"))
    if is_verified is not None:
        query = query.filter(schema.Company.is_verified == is_verified)

    total = query.count()
    results = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "results": results
    }

# Read one
@router.get("/{company_id}")
def read_one(company_id: int, db: Session = Depends(get_db)):
    item = db.query(schema.Company).filter(schema.Company.id == company_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Company not found")
    return item

# Update one
@router.put("/{company_id}")
def update_one(company_id: int, updates: dict, db: Session = Depends(get_db)):
    item = db.query(schema.Company).filter(schema.Company.id == company_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Company not found")
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
        item = db.query(schema.Company).filter(schema.Company.id == entry["id"]).first()
        if item:
            for key, value in entry.items():
                if key != "id":
                    setattr(item, key, value)
            updated.append(item)
    db.commit()
    return updated

# Delete one
@router.delete("/{company_id}")
def delete_one(company_id: int, db: Session = Depends(get_db)):
    item = db.query(schema.Company).filter(schema.Company.id == company_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Company not found")
    db.delete(item)
    db.commit()
    return { "message": "Deleted successfully." }

# Delete multiple
@router.delete("/")
def delete_multiple(ids: list[int], db: Session = Depends(get_db)):
    db.query(schema.Company).filter(schema.Company.id.in_(ids)).delete(synchronize_session=False)
    db.commit()
    return { "message": "Multiple companies deleted successfully." }

# Verify company manually
@router.post("/{company_id}/verify")
def mark_verified(company_id: int, db: Session = Depends(get_db)):
    item = db.query(schema.Company).filter(schema.Company.id == company_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Company not found")
    item.is_verified = 1
    db.commit()
    return { "message": f"Company '{item.name}' marked as verified." }
