from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database import init_db
from app.routers import auth, transactions, analytics, users

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    ## Finance System API
    A professional finance tracking system backend.

    ### Features
    - 💰 Track income and expenses
    - 📊 Financial health score
    - 📈 Analytics and summaries
    - 👥 Role based access control
    - 🔐 JWT Authentication
    """,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(analytics.router)


@app.on_event("startup")
def startup_event():
    """Initialize database on startup."""
    init_db()
    print("✅ Database initialized")
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} is running")


@app.get("/", tags=["Root"])
def root():
    """Root endpoint — API health check."""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health", tags=["Root"])
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}