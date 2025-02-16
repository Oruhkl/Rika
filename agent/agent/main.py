from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.web3 import client
from app.routes.agent import agent
from app.routes.celery import celery


import os

app = FastAPI(title="RikaPayroll API", version="1.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(client.router, prefix="/api/v1/payroll", tags=["payroll"])
app.include_router(agent.router, prefix="/api/v1/agent", tags=["agent"])
app.include_router(celery.router, prefix="/api/v1/celery", tags=["celery"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )