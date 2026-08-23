import uvicorn
import os
import sys
import socket

if __name__ == "__main__":
    # Ensure current directory is in sys.path
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Get local LAN IP address for mobile phone access
    local_ip = "127.0.0.1"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        pass
        
    print("=" * 70)
    print(">> ADAPTIVE AI-BASED PLACEMENT READINESS SYSTEM")
    print("   Personalized Skill-Gap Detection & Explainable AI")
    print("=" * 70)
    print(f">> Local PC Access:     http://localhost:8000")
    print(f">> Mobile Phone Access:  http://{local_ip}:8000")
    print(f">> API Documentation:    http://localhost:8000/docs")
    print("=" * 70)
    
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)

