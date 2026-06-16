"""Mock API server for testing BuildSmart AI frontend"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import json
from datetime import datetime, timedelta
import jwt

app = FastAPI(
    title="BuildSmart AI Mock API",
    version="1.0.0",
    description="Mock API for testing"
)

# Add CORS middleware to allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class UserCreate(BaseModel):
    name: Optional[str] = Field(default=None)
    full_name: Optional[str] = Field(default=None)
    email: EmailStr
    password: str
    role: str = "user"
    
    class Config:
        populate_by_name = True
    
    def get_full_name(self):
        return self.full_name or self.name or "Unknown User"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class ProjectCreate(BaseModel):
    project_name: str
    country: str
    state: str
    city: str
    postal_code: str
    locality: str
    plot_area: float
    construction_area: float
    building_type: str
    floors: int
    material_type: str
    design_style: str
    budget: float

class ProjectResponse(BaseModel):
    id: int
    project_name: str
    country: str
    state: str
    city: str
    postal_code: str
    locality: str
    plot_area: float
    construction_area: float
    building_type: str
    floors: int
    material_type: str
    design_style: str
    budget: float
    created_at: str
    user_id: int

class DesignGenerateRequest(BaseModel):
    project_id: int = 1
    plot_area: float
    construction_area: float
    building_type: str
    floors: int
    design_style: str
    budget: float = 0
    include_3d: bool = False

class RoomInfo(BaseModel):
    room_name: str
    length: float
    width: float

class FloorInfo(BaseModel):
    floor_name: str
    rooms: list

class DesignMetadata(BaseModel):
    style: str
    building_type: str
    total_construction_area: float
    total_floors: int

class DesignResponse(BaseModel):
    id: int
    project_id: int
    floor_plan_url: str
    exterior_concept_url: str
    interior_concept_url: str
    design_style: str
    design_metadata: dict
    ground_floor: dict
    upper_floors: list
    created_at: str

# Mock database
mock_projects = {}
mock_project_counter = 0
mock_users = {
    "test@example.com": {
        "id": 1,
        "full_name": "Test User",
        "email": "test@example.com",
        "password": "Test123!@#",
        "role": "Individual"
    }
}
mock_designs = {}
mock_design_counter = 0

SECRET_KEY = "your-super-secret-key-change-in-production"
ALGORITHM = "HS256"

def create_access_token(user_id: int, email: str, expires_delta: Optional[timedelta] = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    
    to_encode = {"sub": str(user_id), "email": email, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.get("/")
async def root():
    return {"message": "BuildSmart AI Mock API is running"}

@app.post("/api/v1/auth/register", response_model=TokenResponse)
async def register(user: UserCreate):
    # Check if user already exists
    if user.email in mock_users:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    user_id = len(mock_users) + 1
    full_name = user.get_full_name()
    mock_users[user.email] = {
        "id": user_id,
        "full_name": full_name,
        "email": user.email,
        "password": user.password,
        "role": user.role
    }
    
    # Create token
    access_token = create_access_token(user_id, user.email)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user_id,
            "full_name": full_name,
            "email": user.email,
            "role": user.role
        }
    }

@app.post("/api/v1/auth/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    if credentials.email not in mock_users:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user = mock_users[credentials.email]
    if user["password"] != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create token
    access_token = create_access_token(user["id"], user["email"])
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "full_name": user["full_name"],
            "email": user["email"],
            "role": user["role"]
        }
    }

@app.get("/api/v1/auth/me", response_model=UserResponse)
async def get_current_user(token: str = None):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        if not email or email not in mock_users:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = mock_users[email]
        return {
            "id": user["id"],
            "full_name": user["full_name"],
            "email": user["email"],
            "role": user["role"]
        }
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

# Project endpoints
@app.post("/api/v1/projects", response_model=ProjectResponse)
async def create_project(project: ProjectCreate):
    global mock_project_counter
    mock_project_counter += 1
    project_id = mock_project_counter
    
    project_data = {
        "id": project_id,
        **project.dict(),
        "created_at": datetime.utcnow().isoformat(),
        "user_id": 1  # Default user for mock
    }
    
    mock_projects[project_id] = project_data
    return project_data

@app.get("/api/v1/projects/")
async def list_projects():
    return {"projects": list(mock_projects.values()), "total": len(mock_projects)}

@app.get("/api/v1/projects/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int):
    if project_id not in mock_projects:
        raise HTTPException(status_code=404, detail="Project not found")
    return mock_projects[project_id]

@app.put("/api/v1/projects/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: int, project: ProjectCreate):
    if project_id not in mock_projects:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project_data = {
        "id": project_id,
        **project.dict(),
        "created_at": mock_projects[project_id]["created_at"],
        "user_id": mock_projects[project_id]["user_id"]
    }
    
    mock_projects[project_id] = project_data
    return project_data

@app.delete("/api/v1/projects/{project_id}")
async def delete_project(project_id: int):
    if project_id not in mock_projects:
        raise HTTPException(status_code=404, detail="Project not found")
    del mock_projects[project_id]
    return {"message": "Project deleted"}

# Design endpoints
@app.post("/api/v1/design/generate")
async def generate_design(request: DesignGenerateRequest):
    global mock_design_counter
    mock_design_counter += 1
    design_id = mock_design_counter
    
    # Generate SVG data URIs for images
    floor_plan_svg = f"""data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Crect width='400' height='300' fill='%23f0f0f0'/%3E%3Ctext x='50' x='50' font-size='16' fill='%23333'%3EFloor Plan - {request.building_type}%3C/text%3E%3Crect x='20' y='50' width='150' height='100' fill='%23e0e0ff' stroke='%23333'/%3E%3Ctext x='50' y='110' font-size='12'%3ELiving Room%3C/text%3E%3Crect x='200' y='50' width='100' height='100' fill='%23ffe0e0' stroke='%23333'/%3E%3Ctext x='210' y='110' font-size='12'%3EKitchen%3C/text%3E%3C/svg%3E"""
    exterior_svg = f"""data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Crect width='400' height='300' fill='%23e0f0ff'/%3E%3Ctext x='50' y='50' font-size='16' fill='%23333'%3E3D Exterior - {request.design_style}%3C/text%3E%3Cpolygon points='100,200 200,80 300,200' fill='%23ff9999' stroke='%23333' stroke-width='2'/%3E%3Crect x='150' y='150' width='40' height='50' fill='%23ffff99'/%3E%3C/svg%3E"""
    interior_svg = f"""data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Crect width='400' height='300' fill='%23fff0e0'/%3E%3Ctext x='50' y='50' font-size='16' fill='%23333'%3EInterior - {request.floors} Floors%3C/text%3E%3Crect x='50' y='80' width='300' height='180' fill='%23ffffff' stroke='%23333'/%3E%3Cline x1='200' y1='80' x2='200' y2='260' stroke='%23999' stroke-width='2'/%3E%3C/svg%3E"""
    
    design_data = {
        "id": design_id,
        "project_id": request.project_id,
        "floor_plan_url": floor_plan_svg,
        "exterior_concept_url": exterior_svg,
        "interior_concept_url": interior_svg,
        "design_style": request.design_style,
        "design_metadata": {
            "style": request.design_style,
            "building_type": request.building_type,
            "total_construction_area": request.construction_area,
            "total_floors": request.floors
        },
        "ground_floor": {
            "floor_name": "Ground Floor",
            "rooms": [
                {"room_name": "Living Room", "length": 25.0, "width": 20.0},
                {"room_name": "Kitchen", "length": 15.0, "width": 12.0},
                {"room_name": "Dining Room", "length": 18.0, "width": 16.0},
                {"room_name": "Bathroom", "length": 8.0, "width": 6.0},
            ]
        },
        "upper_floors": [
            {
                "floor_name": f"Floor {i}",
                "rooms": [
                    {"room_name": f"Bedroom {i}-1", "length": 16.0, "width": 14.0},
                    {"room_name": f"Bedroom {i}-2", "length": 14.0, "width": 12.0},
                    {"room_name": f"Bathroom {i}", "length": 8.0, "width": 6.0},
                    {"room_name": f"Hallway {i}", "length": 12.0, "width": 8.0},
                ]
            }
            for i in range(2, request.floors + 1)
        ],
        "created_at": datetime.utcnow().isoformat()
    }
    
    mock_designs[design_id] = design_data
    return design_data

# Cost prediction endpoint
@app.post("/api/v1/cost/predict")
async def predict_cost(data: dict):
    # Simple mock cost calculation
    estimated_cost = data.get("construction_area", 0) * 150  # $150 per sqft
    return {
        "estimated_cost": estimated_cost,
        "currency": "USD",
        "breakdown": {
            "material": estimated_cost * 0.4,
            "labor": estimated_cost * 0.35,
            "equipment": estimated_cost * 0.25
        }
    }

# BOQ generation endpoint
@app.post("/api/v1/boq/generate")
async def generate_boq(data: dict):
    return {
        "boq_id": 1,
        "items": [
            {"item": "Concrete", "quantity": 100, "unit": "cubic meters", "rate": 250, "total": 25000},
            {"item": "Steel", "quantity": 50, "unit": "metric tons", "rate": 500, "total": 25000},
            {"item": "Labor", "quantity": 1000, "unit": "hours", "rate": 50, "total": 50000}
        ]
    }

# Timeline prediction endpoint
@app.post("/api/v1/timeline/predict")
async def predict_timeline(data: dict):
    construction_area = data.get("construction_area", 0)
    months = max(6, construction_area / 5000)  # Rough estimate
    return {
        "estimated_duration": months,
        "unit": "months",
        "phases": [
            {"phase": "Excavation", "duration": 2},
            {"phase": "Foundation", "duration": 3},
            {"phase": "Structure", "duration": int(months) - 8},
            {"phase": "Finishing", "duration": 3}
        ]
    }

# Risk analysis endpoint
@app.post("/api/v1/risk/analyze")
async def analyze_risk(data: dict):
    return {
        "risk_score": 0.35,
        "risk_level": "Low",
        "risks": [
            {"risk": "Weather delays", "probability": 0.3, "impact": "Medium"},
            {"risk": "Material shortage", "probability": 0.2, "impact": "High"},
            {"risk": "Labor availability", "probability": 0.25, "impact": "Medium"}
        ]
    }

# Chat endpoint
@app.post("/api/v1/chat/ask")
async def chat_ask(data: dict):
    question = data.get("question", "")
    return {
        "response": f"Thank you for your question: '{question}'. This is a mock response from the BuildSmart AI assistant."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8004)
