from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from typing import Optional
from simulator import corridor_simulator

router = APIRouter(prefix="/api", tags=["Trains & Simulator"])

class ConnectionRiskRequest(BaseModel):
    incoming_train_id: str
    connecting_train_id: str
    scheduled_buffer_mins: int = 40
    sim_date: Optional[str] = "2025-07-15"

class WhatIfSimulationRequest(BaseModel):
    prioritize_rajdhani: bool = True
    emergency_block_mins: float = 0.0
    emergency_block_section: str = "Agra-Gwalior"
    sim_date: Optional[str] = "2025-07-15"

@router.get("/trains")
def get_all_trains(sim_date: str = Query("2025-07-15", description="Historical weather date")):
    """Get all corridor trains with current positions and probabilistic ETA"""
    return corridor_simulator.get_all_trains(sim_date)

@router.get("/trains/{train_id}")
def get_train_by_id(train_id: str, sim_date: str = Query("2025-07-15")):
    """Get detailed train info, milestone route, and XAI delay breakdown"""
    trains = corridor_simulator.get_all_trains(sim_date)
    found = next((t for t in trains if t["id"] == train_id or t["number"] == train_id), None)
    if not found:
        raise HTTPException(status_code=404, detail="Train not found")
    return found

@router.post("/trains/connection-risk")
def evaluate_connection_risk(req: ConnectionRiskRequest):
    """Calculates transfer buffer risk between connecting trains and suggests alternatives"""
    return corridor_simulator.evaluate_connection_risk(
        req.incoming_train_id,
        req.connecting_train_id,
        req.scheduled_buffer_mins,
        req.sim_date
    )

@router.post("/simulate/what-if")
def run_what_if(req: WhatIfSimulationRequest):
    """Dispatcher What-If Precedence & Emergency Maintenance Block Simulator"""
    return corridor_simulator.run_what_if_simulation(
        prioritize_rajdhani=req.prioritize_rajdhani,
        emergency_block_mins=req.emergency_block_mins,
        emergency_block_section=req.emergency_block_section,
        sim_date=req.sim_date
    )

@router.get("/simulate/cascade-graph")
def get_cascade_graph():
    """Directed node graph visualizing downstream ripple effect of delays"""
    return corridor_simulator.get_delay_cascade_graph()

@router.get("/simulate/platform-clashes")
def get_platform_clashes():
    """Flags junction platform overlaps and recommends unoccupied loop lines"""
    return corridor_simulator.get_platform_clash_predictions()
