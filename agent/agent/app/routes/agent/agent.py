from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, APIRouter
from app.routes.agent.model import AgentOutputSchema, AgentInteractRequest, ParameterRequestSchema, AgentOutputSchemaWithParameterRequest  
from app.agent import RikaAgent
import uuid
import logging
import httpx
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware

# Load .env file
load_dotenv()
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

# Set up logging
logger = logging.getLogger("rika_agent")
logging.basicConfig(level=logging.INFO)

# Base URL of your FastAPI application
FASTAPI_BASE_URL = "http://localhost:8000"
router = APIRouter()

agent = RikaAgent(anthropic_api_key)

# Enable CORS for WebSocket
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (adjust for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@router.post("/agent/interact", response_model=AgentOutputSchemaWithParameterRequest)
async def agent_interact(request: AgentInteractRequest):
    """Endpoint for interacting with Rika, the payroll assistant (HTTP)."""
    session_id = request.session_id or str(uuid.uuid4())
    return await agent.process_prompt(request.prompt_text, session_id, request.employer_address)

@router.websocket("/ws/{employer_address}")
async def websocket_endpoint(websocket: WebSocket, employer_address: str):
    await websocket.accept()
    session_id = str(uuid.uuid4())
    agent.conversation_store[session_id] = []

    try:
        while True:
            user_prompt = await websocket.receive_text()
            logger.info(f"Received message: {user_prompt}")
            
            # Process prompt with employer_address
            response = await agent.process_prompt(user_prompt, session_id, employer_address)
            
            json_response = {
                "api_route": response.get("api_route"),
                "parameters": response.get("parameters"),
                "error": response.get("error"),
                "api_response": response.get("api_response"), 
                "parameter_request": response.get("parameter_request").dict() if response.get("parameter_request") else None,
                "session_id": session_id,
                "help_buttons": response.get("help_buttons", [])
            }
            
            await websocket.send_json(json_response)
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: {session_id}")
    finally:
        if session_id in agent.conversation_store:
            del agent.conversation_store[session_id]


def get_router():
    return router
