import sys
import os
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# --- 1. PATH SETUP ---
# Ensures Python finds 'train_brain' outside the 'Backend' folder
BASE_DIR = Path(__file__).resolve().parent 
PROJECT_ROOT = BASE_DIR.parent              

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# --- 2. IMPORT AI MODULES ---
try:
    from train_brain import use_ai
    from train_brain import auto_assigner
    from train_brain import sprint_report
    print("✅ AI Engine: train_brain modules connected.")
except Exception as e:
    print(f"❌ CRITICAL LOAD FAILURE: {e}")
    sys.exit(1)

# --- 3. APP CONFIG ---
load_dotenv()
app = FastAPI(title="OptiSprint AI Engine")

# CORS for direct browser testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static folder for the generated Seaborn/Matplotlib charts
static_dir = PROJECT_ROOT / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# --- 4. DATA SCHEMAS (Matches React JSON) ---
class TaskItem(BaseModel):
    task_id: int
    story_points: int

class PredictionRequest(BaseModel):
    tasks: List[TaskItem]
    current_team_load: float
    deadline_limit: Optional[float] = 40.0

# --- 5. ENDPOINTS ---

@app.get("/")
async def health_check():
    return {"status": "online", "engine": "ML Inference Active", "docs": "/docs"}

@app.post("/api/predict-sprint")
async def predict(data: PredictionRequest):
    try:
        # 1. Get results from AI logic
        results = use_ai.process_tasks(data.tasks, data.current_team_load, data.deadline_limit)
        
        # 2. Check if results is actually a list (CRITICAL FIX)
        if not isinstance(results, list):
            print(f"❌ AI Logic returned non-list: {results}")
            raise HTTPException(status_code=500, detail="AI engine returned an invalid format.")

        # 3. Defensive calculation
        try:
            total_time = sum(task.get('ai_option', {}).get('hours', 0) for task in results)
            max_risk = max((task.get('ai_option', {}).get('risk', 0) for task in results), default=0)
        except Exception as calc_err:
            print(f"❌ Calculation Error: {calc_err}")
            raise HTTPException(status_code=500, detail="Error calculating sprint metrics.")

        return {
            "predicted_time": round(total_time, 2),
            "risk_score": round(max_risk / 100, 2),
            "tasks": results,
            "status": "success"
        }

    except Exception as e:
        # This will now print the EXACT line and error in your terminal
        import traceback
        traceback.print_exc() 
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/api/auto-assign")
async def assign():
    """Triggers the Greedy Algorithm in auto_assigner.py"""
    try:
        result = auto_assigner.run_auto_assignment()
        return {"status": "success", "data": result}
    except Exception as e:
        print(f"❌ Assignment Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sprint-report")
async def get_report():
    """Generates the visual workload chart and returns metrics"""
    try:
        result = sprint_report.generate_sprint_analytics()
        
        # Ensure the frontend can find the image via the static mount
        if result.get("status") != "error" and "report_url" in result:
            # Convert local path to web-accessible path
            filename = os.path.basename(result['report_url'])
            result["report_url"] = f"/static/{filename}"
            
        return result
    except Exception as e:
        print(f"❌ Report Error: {e}")
        raise HTTPException(status_code=404, detail="Could not generate analytics report")

if __name__ == "__main__":
    import uvicorn
    # Hardcoded to port 8000 to match Vite Proxy settings
    uvicorn.run(app, host="127.0.0.1", port=8000)