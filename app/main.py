"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import init_db
from app.routes import auth, updates, style, drafts, review, send, dashboard, audience

# Initialize database on startup
init_db()

# Create FastAPI app
app = FastAPI(
    title="StakeSync - Weekly Business Update Automation",
    description="Automate weekly business updates with AI-powered draft generation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(updates.router)
app.include_router(style.router)
app.include_router(drafts.router)
app.include_router(review.router)
app.include_router(send.router)
app.include_router(dashboard.router)
app.include_router(audience.router)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to StakeSync API",
        "docs": "/docs",
        "chatbot": "/static/chatbot.html"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    from app.config import get_settings
    
    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )
