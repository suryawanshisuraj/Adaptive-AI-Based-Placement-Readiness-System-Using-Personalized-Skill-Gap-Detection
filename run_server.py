import uvicorn
import os
import sys

if __name__ == "__main__":
    # Ensure current directory is in sys.path
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
        
    print("=" * 70)
    print(">> ADAPTIVE AI-BASED PLACEMENT READINESS SYSTEM")
    print("   Personalized Skill-Gap Detection & Explainable AI")
    print("=" * 70)
    print(">> Web Interface: http://127.0.0.1:8000")
    print(">> API Documentation: http://127.0.0.1:8000/docs")
    print("=" * 70)
    
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)
