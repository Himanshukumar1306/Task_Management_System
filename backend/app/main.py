
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth_router, employee_router, task_router, dashboard_router
from app.config import settings
from app.database import engine, Base

# Create tables if they don't exist (useful for quick start, though alembic is better)
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(employee_router)
app.include_router(task_router)
app.include_router(dashboard_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

