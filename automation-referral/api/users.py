from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from database.db import SessionLocal
from models.schema import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a user
@router.post("/")
def create_user(payload: dict, db: Session = Depends(get_db)):
    item = User(**payload)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# List users with filters and pagination
@router.get("/")
def list_users(
    name: str = Query(None),
    email: str = Query(None),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(User)

    if name:
        query = query.filter(User.name.ilike(f"%{name}%"))
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))

    total = query.count()
    results = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "results": results
    }

# Get a single user
@router.get("/{user_id}")
def read_one(user_id: int, db: Session = Depends(get_db)):
    item = db.query(User).filter(User.id == user_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="User not found")
    return item

# Update one user
@router.put("/{user_id}")
def update_one(user_id: int, updates: dict, db: Session = Depends(get_db)):
    item = db.query(User).filter(User.id == user_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in updates.items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

# Update multiple users
@router.put("/")
def update_multiple(updates: list[dict], db: Session = Depends(get_db)):
    updated = []
    for entry in updates:
        item = db.query(User).filter(User.id == entry["id"]).first()
        if item:
            for key, value in entry.items():
                if key != "id":
                    setattr(item, key, value)
            updated.append(item)
    db.commit()
    return updated

# Delete one user
@router.delete("/{user_id}")
def delete_one(user_id: int, db: Session = Depends(get_db)):
    item = db.query(User).filter(User.id == user_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(item)
    db.commit()
    return { "message": "User deleted successfully." }

# Delete multiple users
@router.delete("/")
def delete_multiple(ids: list[int], db: Session = Depends(get_db)):
    db.query(User).filter(User.id.in_(ids)).delete(synchronize_session=False)
    db.commit()
    return { "message": "Multiple users deleted successfully." }
