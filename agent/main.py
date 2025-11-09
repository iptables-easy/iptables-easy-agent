from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from agent.config import settings
from agent.iptables_executor import IptablesExecutor
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import asyncio
import aiohttp
import sys
import os

app = FastAPI(
    title="iptables-easy Agent",
    description="Agent for executing iptables rules on nodes",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Schemas
class RuleRequest(BaseModel):
    chain: str
    action: str
    protocol: Optional[str] = None
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    port: Optional[int] = None


class RuleDeleteRequest(BaseModel):
    chain: str
    action: str
    protocol: Optional[str] = None
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    port: Optional[int] = None


class HeartbeatRequest(BaseModel):
    agent_token: str
    status: str = "online"
    system_info: Optional[dict] = None


# Routes
@app.get("/")
def read_root():
    return {"message": "iptables-easy Agent is running", "agent_name": settings.AGENT_NAME}


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "agent_name": settings.AGENT_NAME,
        "timestamp": datetime.utcnow()
    }


@app.post("/rules/add")
def add_rule(rule: RuleRequest):
    result = IptablesExecutor.add_rule(
        chain=rule.chain,
        action=rule.action,
        protocol=rule.protocol,
        source_ip=rule.source_ip,
        destination_ip=rule.destination_ip,
        port=rule.port
    )
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result


@app.post("/rules/delete")
def delete_rule(rule: RuleDeleteRequest):
    result = IptablesExecutor.delete_rule(
        chain=rule.chain,
        action=rule.action,
        protocol=rule.protocol,
        source_ip=rule.source_ip,
        destination_ip=rule.destination_ip,
        port=rule.port
    )
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result


@app.get("/rules/list")
def list_rules(chain: Optional[str] = None):
    result = IptablesExecutor.list_rules(chain=chain)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result


@app.post("/rules/flush")
def flush_rules(chain: str):
    result = IptablesExecutor.flush_chain(chain=chain)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result


@app.post("/rules/save")
def save_rules():
    result = IptablesExecutor.save_rules()
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result


@app.post("/heartbeat")
def send_heartbeat(heartbeat: HeartbeatRequest):
    # This endpoint would be called by the agent to send heartbeat
    # In a real implementation, this would update the node status in the backend
    return {"message": "Heartbeat received", "status": "online"}
