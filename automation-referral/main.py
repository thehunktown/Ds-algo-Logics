# rag_referral_agent/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import jobs, referrals, companies, users
from database.db import Base, engine

# Initialize FastAPI app
app = FastAPI(
    title="RAG-Based Referral Agent",
    description="Backend API for job referral automation using LLaMA and LangChain",
    version="1.0.0",
)

# Setup CORS for Streamlit/frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables in the database
Base.metadata.create_all(bind=engine)

# Register API routers
app.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
app.include_router(referrals.router, prefix="/referrals", tags=["Referrals"])
app.include_router(companies.router, prefix="/companies", tags=["Companies"])
app.include_router(users.router, prefix="/users", tags=["Users"])

# Root endpoint
@app.get("/")
def root():
    return {"message": "RAG Referral Agent API is running."}
