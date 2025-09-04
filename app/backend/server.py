from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import logging
from pathlib import Path

# Import database and routes
from database import db, close_db_connection
from routes.contact import router as contact_router

# Create the main app without a prefix
app = FastAPI(
    title="Shubham Kadam Portfolio API",
    description="Backend API for portfolio website",
    version="1.0.0"
)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Add contact routes
api_router.include_router(contact_router, tags=["contact"])

# Health check endpoint
@api_router.get("/")
async def root():
    return {"message": "Portfolio API is running", "version": "1.0.0"}

@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}

# Include the router in the main app
app.include_router(api_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_db_connection()

# Create uploads directory
uploads_dir = Path("/app/backend/uploads")
uploads_dir.mkdir(exist_ok=True)