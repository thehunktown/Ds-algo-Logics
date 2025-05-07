from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from database.db import SessionLocal
from models.schema import Job

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create one
@router.post("/")
def create_job(payload: dict, db: Session = Depends(get_db)):
    item = Job(**payload)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# List all jobs with rich filters
@router.get("/")
def list_jobs(
    role: str = Query(None),
    company_name: str = Query(None),
    posted_by: str = Query(None),
    status: str = Query(None),
    critical: int = Query(None),
    received_call: int = Query(None),  # 0 or 1
    reminder_sent: int = Query(None),  # 0 or 1
    created_after: str = Query(None),
    active_till_before: str = Query(None),
    sort_by: str = Query("created_at"),
    order: str = Query("desc"),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(Job)

    if role:
        query = query.filter(Job.role.ilike(f"%{role}%"))
    if company_name:
        query = query.filter(Job.company_name.ilike(f"%{company_name}%"))
    if posted_by:
        query = query.filter(Job.posted_by.ilike(f"%{posted_by}%"))
    if status:
        query = query.filter(Job.status == status)
    if critical is not None:
        query = query.filter(Job.critical == critical)
    if received_call is not None:
        query = query.filter(Job.received_call == received_call)
    if reminder_sent is not None:
        query = query.filter(Job.reminder_sent == reminder_sent)
    if created_after:
        query = query.filter(Job.created_at >= created_after)
    if active_till_before:
        query = query.filter(Job.active_till <= active_till_before)

    if hasattr(Job, sort_by):
        sort_attr = getattr(Job, sort_by)
        query = query.order_by(desc(sort_attr) if order == "desc" else asc(sort_attr))

    total = query.count()
    results = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "results": results
    }

# Get single job
@router.get("/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

# Update one
@router.put("/{job_id}")
def update_job(job_id: int, updates: dict, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    for key, value in updates.items():
        setattr(job, key, value)
    db.commit()
    db.refresh(job)
    return job

# Update multiple
@router.put("/")
def update_multiple_jobs(jobs: list[dict], db: Session = Depends(get_db)):
    updated = []
    for entry in jobs:
        job = db.query(Job).filter(Job.id == entry["id"]).first()
        if job:
            for key, value in entry.items():
                if key != "id":
                    setattr(job, key, value)
            updated.append(job)
    db.commit()
    return updated

# Delete one
@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return {"message": "Deleted successfully"}

# Delete multiple
@router.delete("/")
def delete_multiple(ids: list[int], db: Session = Depends(get_db)):
    db.query(Job).filter(Job.id.in_(ids)).delete(synchronize_session=False)
    db.commit()
    return {"message": "Multiple jobs deleted"}
