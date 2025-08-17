# 🌊 Flood Detection System

An AI-powered flood risk assessment system that analyzes coordinates and terrain images to provide intelligent flood risk predictions using Google's Gemini AI.

## ✨ Features

- **📍 Coordinate Analysis**: Input latitude/longitude for location-based flood risk assessment
- **🖼️ Image Analysis**: Upload terrain images for AI-powered visual flood risk analysis
- **🗺️ Interactive Map**: Free Leaflet/OpenStreetMap integration with risk visualization
- **🤖 AI-Powered**: Uses Google Gemini 2.0 Flash for intelligent analysis
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices
- **🎨 Modern UI**: Built with Next.js, Tailwind CSS, and shadcn/ui components

## 🚀 Tech Stack

### Frontend
- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **shadcn/ui** - UI components
- **Leaflet** - Free mapping (OpenStreetMap)
- **React Leaflet** - React integration for maps

### Backend
- **FastAPI** - Python web framework
- **Google Gemini AI** - AI analysis engine
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **PIL (Pillow)** - Image processing

## 🛠️ Installation

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- Google Gemini API key

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/flood-detection-system.git
cd flood-detection-system
```

### 2. Frontend Setup
```bash
# Install dependencies
npm install

# Create environment file
cp .env.local.example .env.local
# Edit .env.local and add your configuration
```

### 3. Backend Setup
```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn google-generativeai python-dotenv pillow python-multipart

# Create environment file
cp .env.example .env
# Edit .env and add your Gemini API key
```

### 4. Get API Keys

#### Google Gemini AI (Required)
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add to `backend/.env`:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## 🚀 Running the Application

### Start Backend Server
```bash
cd backend
python start.py
```
Backend will run on `http://localhost:8001`

### Start Frontend Server
```bash
npm run dev
```
Frontend will run on `http://localhost:3000`

## 📖 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

### Endpoints

#### `POST /api/analyze/coordinates`
Analyze flood risk based on coordinates
```json
{
  "latitude": 40.7128,
  "longitude": -74.0060
}
```

#### `POST /api/analyze/image`
Analyze flood risk based on uploaded terrain image
- Accepts: JPG, PNG, GIF (max 10MB)

## 🎯 Usage

1. **Coordinate Analysis**:
   - Enter latitude and longitude
   - Click "Analyze Coordinates"
   - View risk assessment and map visualization

2. **Image Analysis**:
   - Upload a terrain/landscape image
   - Click "Analyze Image"
   - Get AI-powered flood risk assessment

3. **Interactive Map**:
   - View analyzed locations with risk-colored markers
   - Pan and zoom to explore terrain
   - Click markers for detailed information

## 🌍 Deployment

### Frontend (Vercel)
```bash
npm run build
# Deploy to Vercel, Netlify, or your preferred platform
```

### Backend (Railway/Render)
```bash
# Add Procfile for deployment
echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > backend/Procfile
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI for intelligent analysis
- OpenStreetMap for free mapping data
- Leaflet for excellent mapping library
- shadcn/ui for beautiful components

## 📞 Support

If you have any questions or need help, please open an issue on GitHub.

---

**⚠️ Note**: This system provides risk assessments for informational purposes. Always consult official weather services and local authorities for emergency planning.