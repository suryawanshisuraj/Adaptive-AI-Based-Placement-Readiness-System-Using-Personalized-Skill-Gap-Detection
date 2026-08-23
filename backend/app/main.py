import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse

from .database import init_db
from .api.routes_profile import router as profile_router
from .api.routes_assessment import router as assessment_router
from .api.routes_analytics import router as analytics_router
from .api.routes_roadmap import router as roadmap_router
from .api.routes_research import router as research_router
from .api.routes_interview import router as interview_router
from .api.routes_resume import router as resume_router

app = FastAPI(
    title="Adaptive AI-Based Placement Readiness System",
    description="Personalized Skill-Gap Detection, Explainable AI, and Adaptive Learning Path Generator",
    version="1.0.0"
)

# Enable CORS — allow all origins (covers localhost dev + Vercel production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(profile_router)
app.include_router(assessment_router)
app.include_router(analytics_router)
app.include_router(roadmap_router)
app.include_router(research_router)
app.include_router(interview_router)
app.include_router(resume_router)

# Resolve frontend directory path (works both locally and on Vercel)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")

# Mount static assets — serves /static/css/style.css, /static/js/*.js, etc.
# This works locally; on Vercel, vercel.json routes handle it
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.on_event("startup")
def on_startup():
    init_db()

def _serve_page(filename: str):
    file_path = os.path.join(FRONTEND_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(
            file_path,
            media_type="text/html",
            headers={"Cache-Control": "no-cache, no-store, must-revalidate", "Pragma": "no-cache", "Expires": "0"}
        )
    return HTMLResponse(f"<h1>{filename} not found</h1>", status_code=404)

@app.get("/auth", include_in_schema=False)
def serve_auth():
    return _serve_page("auth.html")

@app.get("/landing", include_in_schema=False)
def serve_landing():
    return _serve_page("landing.html")

@app.get("/about", include_in_schema=False)
def serve_about():
    return _serve_page("about.html")

@app.get("/assessment", include_in_schema=False)
def serve_assessment():
    return _serve_page("assessment.html")

@app.get("/interview", include_in_schema=False)
def serve_interview():
    return _serve_page("interview.html")

@app.get("/resume", include_in_schema=False)
def serve_resume():
    return _serve_page("resume.html")

@app.get("/roadmap", include_in_schema=False)
def serve_roadmap():
    return _serve_page("roadmap.html")

@app.get("/404", include_in_schema=False)
def serve_404():
    return _serve_page("404.html")

@app.get("/", include_in_schema=False)
def serve_index():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(
            index_path,
            media_type="text/html",
            headers={"Cache-Control": "no-cache, no-store, must-revalidate", "Pragma": "no-cache", "Expires": "0"}
        )
    return {
        "status": "online",
        "system": "Adaptive AI-Based Placement Readiness System",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "placement-readiness-ai"}

