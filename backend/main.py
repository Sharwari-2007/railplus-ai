import asyncio
import os
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from data_loader import weather_loader
from simulator import corridor_simulator, MOCK_TRAINS
from websocket_manager import ws_manager
from routes import trains, weather

# Background telemetry ticker for real-time rake movement & WebSocket broadcast
async def telemetry_ticker():
    while True:
        try:
            await asyncio.sleep(3.0)
            if ws_manager.active_connections:
                # Increment train progress slightly
                for t in MOCK_TRAINS:
                    t["progress_pct"] = (t["progress_pct"] + 0.15) % 100.0
                    if t["remaining_distance_km"] > 5.0:
                        t["remaining_distance_km"] = max(0.0, t["remaining_distance_km"] - 0.8)

                trains_data = corridor_simulator.get_all_trains("2025-07-15")
                payload = {
                    "type": "TELEMETRY_UPDATE",
                    "timestamp": asyncio.get_event_loop().time(),
                    "trains": trains_data
                }
                await ws_manager.broadcast(payload)
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"Error in telemetry ticker: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure dataset exists
    if not os.path.exists(weather_loader.excel_path):
        from generate_dataset import generate_weather_dataset
        generate_weather_dataset()
    
    # Start background ticker task
    ticker_task = asyncio.create_task(telemetry_ticker())
    print("RailPulse AI Backend initialized & Telemetry Ticker started.")
    yield
    ticker_task.cancel()
    print("RailPulse AI Backend shutdown.")

app = FastAPI(
    title="RailPulse AI - Dynamic Forecast of Expected Time of Arrival (ETA)",
    description="Smart India Hackathon SIH26028 - Ministry of Railways",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trains.router)
app.include_router(weather.router)

@app.get("/")
@app.get("/api/health")
@app.get("/health")
def read_root():
    return {
        "system": "RailPulse AI",
        "problem_statement": "SIH26028 - Dynamic Forecast of ETA for Coaching Trains",
        "ministry": "Ministry of Railways",
        "status": "OPERATIONAL",
        "websocket_endpoint": "/ws/live-feed"
    }

@app.websocket("/ws/live-feed")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        # Send initial snapshot immediately upon connecting
        initial_trains = corridor_simulator.get_all_trains("2025-07-15")
        await websocket.send_json({
            "type": "INITIAL_SNAPSHOT",
            "trains": initial_trains
        })
        while True:
            # Keep connection open & listen for optional client ping messages
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
