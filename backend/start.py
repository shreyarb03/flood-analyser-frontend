"""
Startup script for the flood detection API
"""

import uvicorn
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

if __name__=="__main__":
    port=os.getenv("PORT", 8001)
    host=os.getenv("HOST", "0.0.0.0")

    print(f"Starting flood detection Backend API on {host}:{port}")
    print("API documetation is available at")
    print(f"-Swagger UI:http://{host}:{port}/docs")
    print(f"-ReDoc: http://{host}:{port}/redoc")
    print(f"-OpenAPI JSON: http://{host}:{port}/openapi.json")

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info",
    )
