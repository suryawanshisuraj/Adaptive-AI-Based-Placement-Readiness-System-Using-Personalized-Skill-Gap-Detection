from mangum import Mangum
import sys
import os

# Add the project root to path so imports work on Vercel
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.main import app

# Vercel serverless handler
handler = Mangum(app, lifespan="off")
