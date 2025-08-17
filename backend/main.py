from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os
import asyncio
from datetime import datetime
import logging
import google.generativeai as genai
from dotenv import load_dotenv
import base64
import io
import json
import re
from PIL import Image as PILImage

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Gemini AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI(
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class CoordinateRequest(BaseModel):
    latitude: float
    longitude: float

class AnalysisResponse(BaseModel):
    success: bool
    risk_level: str
    description: str
    recommendations: list[str]
    elevation: float
    distance_from_water: float
    message: str

def parse_gemini_response(response_text: str) -> dict:
    """Parse Gemini AI response and extract structured data"""
    try:
        # Try to extract JSON from the response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            parsed_data = json.loads(json_str)
            
            return {
                "risk_level": parsed_data.get("risk_level", "Medium"),
                "description": parsed_data.get("description", "Analysis completed"),
                "recommendations": parsed_data.get("recommendations", []),
                "elevation": parsed_data.get("elevation", 50.0),
                "distance_from_water": parsed_data.get("distance_from_water", 1000.0),
                "image_analysis": parsed_data.get("image_analysis", "")
            }
        else:
            return {
                "risk_level": "Medium",
                "description": "Analysis completed",
                "recommendations": ["Monitor weather conditions", "Stay informed about local alerts"],
                "elevation": 50.0,
                "distance_from_water": 1000.0,
                "image_analysis": response_text
            }
    except Exception as e:
        logger.error(f"Error parsing Gemini response: {str(e)}")
        return {
            "risk_level": "Medium",
            "description": "Analysis completed",
            "recommendations": ["Monitor weather conditions", "Stay informed about local alerts"],
            "elevation": 50.0,
            "distance_from_water": 1000.0,
            "image_analysis": response_text
        }

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Flood Detection API with Gemini AI",
        "version": "1.0.0",
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "ai_model": "Gemini 2.0 Flash",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/analyze/coordinates")
async def analyze_coordinates(request: CoordinateRequest):
    """Analyze flood risk based on coordinates using Gemini AI"""
    try:
        # Create prompt for Gemini AI
        prompt = f"""
        Analyze the flood risk for coordinates: latitude {request.latitude}, longitude {request.longitude}.
        
        Please provide a JSON response with the following structure:
        {{
            "risk_level": "Low|Medium|High|Very High",
            "description": "Detailed description of flood risk factors",
            "recommendations": ["recommendation1", "recommendation2", "recommendation3"],
            "elevation": estimated_elevation_in_meters,
            "distance_from_water": estimated_distance_to_nearest_water_body_in_meters
        }}
        
        Consider factors like:
        - Proximity to water bodies
        - Elevation and topography
        - Historical flood data for the region
        - Climate patterns
        """
        
        # Generate response using Gemini
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content(prompt)
        
        # Parse the response
        parsed_data = parse_gemini_response(response.text)
        
        return {
            "success": True,
            "risk_level": parsed_data["risk_level"],
            "description": parsed_data["description"],
            "recommendations": parsed_data["recommendations"],
            "elevation": parsed_data["elevation"],
            "distance_from_water": parsed_data["distance_from_water"],
            "message": "Coordinate analysis completed successfully"
        }
        
    except Exception as e:
        logger.error(f"Error in coordinate analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/analyze/image")
async def analyze_image(file: UploadFile = File(...)):
    """Analyze flood risk based on uploaded image using Gemini AI"""
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read and process the image
        image_data = await file.read()
        image = PILImage.open(io.BytesIO(image_data))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Create prompt for Gemini AI
        prompt = """
        Analyze this terrain image for flood risk assessment.
        
        Please provide a JSON response with the following structure:
        {
            "risk_level": "Low|Medium|High|Very High",
            "description": "Detailed description of flood risk factors visible in the image",
            "recommendations": ["recommendation1", "recommendation2", "recommendation3"],
            "elevation": estimated_elevation_in_meters,
            "distance_from_water": estimated_distance_to_water_in_meters,
            "image_analysis": "Detailed analysis of what you see in the image"
        }
        
        Consider factors like:
        - Terrain slope and elevation
        - Presence of water bodies
        - Vegetation and land use
        - Drainage patterns
        - Urban development
        - Soil type indicators
        """
        
        # Generate response using Gemini Vision
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content([prompt, image])
        
        # Parse the response
        parsed_data = parse_gemini_response(response.text)
        
        return {
            "success": True,
            "risk_level": parsed_data["risk_level"],
            "description": parsed_data["description"],
            "recommendations": parsed_data["recommendations"],
            "elevation": parsed_data["elevation"],
            "distance_from_water": parsed_data["distance_from_water"],
            "ai_analysis": parsed_data.get("image_analysis", ""),
            "message": "Image analysis completed successfully"
        }
        
    except Exception as e:
        logger.error(f"Error in image analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")



if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    ) 