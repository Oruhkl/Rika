from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# --- Schema Definitions ---
class AgentOutputSchema(BaseModel):
    api_route: Optional[str] = Field(description="The FastAPI route to call.")
    parameters: Optional[Dict[str, Any]] = Field(description="Parameters for the API route.")
    error: Optional[str] = Field(description="Error message if intent is unclear or parameters are missing.")
    api_response: Optional[Dict[str, Any]] = None

class AgentInteractRequest(BaseModel):
    prompt_text: str
    session_id: Optional[str] = None
    employer_address: Optional[str] = Field(None, description="The employer's EVM address.")

class ParameterRequestSchema(BaseModel):
    missing_parameters: List[str]
    api_route_hint: str
    message_to_user: str

class AgentOutputSchemaWithParameterRequest(AgentOutputSchema):
    parameter_request: Optional[ParameterRequestSchema] = None
    session_id: str
    help_buttons: Optional[List[Dict[str, str]]] = None
