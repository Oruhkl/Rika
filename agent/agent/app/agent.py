from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from fastapi import HTTPException
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from app.routes.agent.model import AgentOutputSchema, ParameterRequestSchema, AgentOutputSchemaWithParameterRequest, AgentInteractRequest
from typing import List, Optional, Dict, Any
import logging
import httpx

# Set up logging
logger = logging.getLogger("rika_agent")
logging.basicConfig(level=logging.INFO)

# Base URL of your FastAPI application
FASTAPI_BASE_URL = "http://localhost:8000"

# --- Rika Agent Class ---
class RikaAgent:
    def __init__(self, anthropic_api_key: str):
        self.llm = ChatAnthropic(
            model_name="claude-3-sonnet-20240229",
            anthropic_api_key=anthropic_api_key
        )
        self.conversation_store: Dict[str, List[Dict[str, str]]] = {}

    async def process_prompt(self, user_prompt: str, session_id: str, employer_address: Optional[str] = None) -> Dict[str, Any]:
        """Processes the user prompt, calls the appropriate API, and returns the API response."""
        conversation_history = self.conversation_store.get(session_id, [])
        conversation_context = "\n".join([f"{turn['role']}: {turn['content']}" for turn in conversation_history]) if conversation_history else "No previous conversation."

        # Include the employer_address in the user prompt if provided
        if employer_address:
            user_prompt += f"\nEmployer Address: {employer_address}"

        # Define the prompt template
        prompt_template = PromptTemplate(
            input_variables=["conversation_context", "user_prompt"],
            template=(
                "You are Rika, a helpful Blockchain AI assistant specializing in guiding users to interact effortlessly with Payroll Smart Contracts. "
                "Your primary task is to understand user prompts and determine the correct FastAPI API route to call to manage payroll operations. "
                "You must identify and extract all necessary parameters for each API route. When parameters are missing, you should clearly indicate them to the user in a loving persuasive tone.\n\n"
                "**Conversation History:**\n{conversation_context}\n\n"
                "**New User Prompt:**\n{user_prompt}\n\n"
                "**Task:** Analyze the conversation and the new user prompt to:\n"
                "1. **Determine the User's Intent:** Identify the user's goal related to payroll smart contracts.\n"
                "2. **Match to API Route:** Find the most appropriate FastAPI API route from the list below that matches the user's intent.\n"
                "3. **Parameter Extraction:** Extract all required parameters for the chosen API route from the conversation and new prompt.\n"
                "4. **Handle Missing Parameters:** If any required parameters are missing, identify them.\n"
                "5. **Handle Unclear Intent:** If the user's intent is unclear or doesn't match any API route, recognize this.\n\n"
                "**Available FastAPI API Routes and Required Parameters:**\n"
                "These are the ONLY API routes you can use. Ensure you use the exact route paths and parameter names as listed.\n\n"
                "**Factory Contract Routes (POST Requests - JSON Body):**\n"
                "- `/payroll-contracts` (POST) - **Required:** `employer_address` (e.g., '0x123...')\n\n"
                "**Payroll Contract Routes (POST Requests - JSON Body):**\n"
                "- `/employees` (POST) - **Required:** `name` (e.g., 'John Doe'), `employee_address` (e.g., '0x456...'), `salary` (e.g., 5000), `employer_address` (e.g., '0x123...'), `contract_index` (e.g., 0)\n"
                "- `/funds` (POST) - **Required:** `amount` (e.g., 1000), `employer_address` (e.g., '0x123...'), `contract_index` (e.g., 0)\n"
                "- `/schedules` (POST) - **Required:** `employee_address` (e.g., '0x456...'), `start_date` (e.g., 1672531200), `end_date` (e.g., 1675123200), `interval` (e.g., 0), `employer_address` (e.g., '0x123...'), `contract_index` (e.g., 0)\n"
                "- `/employees/deactivate` (POST) - **Required:** `employee_address` (e.g., '0x456...'), `employer_address` (e.g., '0x123...'), `contract_index` (e.g., 0)\n"
                "- `/employees/reactivate` (POST) - **Required:** `employee_address` (e.g., '0x456...'), `employer_address` (e.g., '0x123...'), `contract_index` (e.g., 0)\n"
                "- `/salaries/update` (POST) - **Required:** `employee_address` (e.g., '0x456...'), `new_salary` (e.g., 6000), `employer_address` (e.g., '0x123...'), `contract_index` (e.g., 0)\n"
                "- `/payrolls/process` (POST) - **Required:** `employer_address` (e.g., '0x123...'), `contract_index` (e.g., 0)\n\n"
                "**Payroll Contract Routes (GET Requests - Query Parameters):**\n"
                "- `/employees/details` (GET) - **Required:** `employee_address` (e.g., '0x456...'), `employer_address` (e.g., '0x123...'), `contract_index` (e.g., 0)\n"
                "- `/employees/all` (GET) - **Required:** `employer_address` (e.g., '0x123...'), `contract_index` (e.g., 0)\n"
                "- `/balance` (GET) - **Required:** `employer_address` (e.g., '0x123...'), `contract_index` (e.g., 0)\n"
                "- `/liability` (GET) - **Required:** `employer_address` (e.g., '0x123...'), `contract_index` (e.g., 0)\n"
                "- `/payrolls/next-date` (GET) - **Required:** `employee_address` (e.g., '0x456...'), `employer_address` (e.g., '0x123...'), `contract_index` (e.g., 0)\n\n"
                "**Response Instructions:**\n"
                "You MUST respond in JSON format, following these guidelines:\n"
                "1. **Missing Parameters:** If you identify missing parameters, respond with:\n"
                '   `{{ "parameters": {{}}, "error": "Missing parameters: [list of missing parameters, comma-separated]" }}`\n'
                "2. **Unclear Intent:** If the user intent is unclear or doesn't match any allowed API route, respond with:\n"
                '   `{{ "parameters": {{}}, "error": "Could not understand your intent. Please clarify your request related to payroll management." }}`\n'
                "3. **Successful Route and Parameter Extraction:** If you successfully determine the API route and have all parameters, respond with ONLY the transaction payload in the 'parameters' field. Set 'api_route' and 'error' to null.\n"
                '   `{{ "parameters": {{ ...transaction payload... }}, "error": null }}`\n'
                "4. **Personality:** Maintain a helpful and clear tone.\n\n"
                "Focus on payroll contract and employee management operations. Do not handle requests outside of these functionalities."
            )
        )

        # Initialize the LLM chain
        chain = LLMChain(llm=self.llm, prompt=prompt_template)

        try:
            # Run the chain
            raw_response = await chain.arun(conversation_context=conversation_context, user_prompt=user_prompt)
            logger.info(f"Raw LLM response: {raw_response}")

            # Parse the response
            base_parser = PydanticOutputParser(pydantic_object=AgentOutputSchema)
            output_parser = OutputFixingParser.from_llm(llm=self.llm, parser=base_parser)
            parsed_response = output_parser.parse(raw_response)

            if parsed_response.error:
                # Handle missing parameters or unclear intent
                if parsed_response.error.startswith("Missing parameters:"):
                    missing_params = parsed_response.error[len("Missing parameters:"):].split(',')
                    missing_params = [param.strip() for param in missing_params]

                    # Generate a friendly message with examples
                    friendly_message = self._generate_friendly_missing_params_message(missing_params)
                    
                    parameter_request = ParameterRequestSchema(
                        missing_parameters=missing_params,
                        api_route_hint=parsed_response.api_route or "Unknown Route",
                        message_to_user=friendly_message
                    )
                    return {
                        "api_route": None,
                        "parameters": {},
                        "error": parameter_request.message_to_user,
                        "parameter_request": parameter_request,
                        "session_id": session_id,
                        "help_buttons": self._generate_help_buttons(missing_params)
                    }
                else:
                    # Handle unclear intent
                    return {
                        "api_route": None,
                        "parameters": {},
                        "error": "I'm sorry, I couldn't quite understand your request. Could you please clarify what you'd like to do with the payroll system?",
                        "parameter_request": None,
                        "session_id": session_id,
                        "help_buttons": []
                    }
            else:
                # Successful route and parameter extraction
                api_response = await self.call_api(parsed_response.api_route, parsed_response.parameters)
                return {
                    "api_route": parsed_response.api_route,
                    "parameters": parsed_response.parameters,
                    "api_response": api_response,
                    "error": None,
                    "parameter_request": None,
                    "session_id": session_id,
                    "help_buttons": []
                }

        except Exception as e:
            logger.error(f"Error processing prompt: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to process prompt: {e}")

    def _generate_friendly_missing_params_message(self, missing_params: List[str]) -> str:
        """Generates a user-friendly message for missing parameters."""
        param_examples = {
            "name": "e.g., 'John Doe'",
            "employee_address": "e.g., '0x456...' (a valid Ethereum address)",
            "salary": "e.g., 5000 (in USD)",
            "contract_index": "e.g., 0 (the index of the payroll contract)",
            "amount": "e.g., 1000 (in USD)",
            "start_date": "e.g., 1672531200 (a Unix timestamp)",
            "end_date": "e.g., 1675123200 (a Unix timestamp)",
            "interval": "e.g., 0 (daily) or 1 (weekly)",
            "new_salary": "e.g., 6000 (in USD)"
        }

        friendly_message = "To proceed, I'll need a bit more information. Could you please provide the following details?\n"
        for param in missing_params:
            example = param_examples.get(param, "a valid value")
            friendly_message += f"- **{param}**: {example}\n"

        friendly_message += "\nOnce you provide these, I'll be able to assist you further!"
        return friendly_message

    def _generate_help_buttons(self, missing_params: List[str]) -> List[Dict[str, str]]:
        """Generates interactive buttons for missing parameters."""
        buttons = []
        for param in missing_params:
            buttons.append({
                "text": f"Provide {param}",
                "value": param
            })
        return buttons

    async def call_api(self, api_route: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Calls the appropriate FastAPI route with the extracted parameters."""
        try:
            # Add the API prefix to the route
            prefixed_route = f"/api/v1/payroll{api_route}"
            
            async with httpx.AsyncClient() as client:
                # POST requests
                if any(api_route.startswith(route) for route in [
                    "/payroll-contracts",
                    "/employees",
                    "/funds",
                    "/schedules",
                    "/employees/deactivate",
                    "/employees/reactivate",
                    "/salaries/update",
                    "/payrolls/process"
                ]):
                    response = await client.post(f"{FASTAPI_BASE_URL}{prefixed_route}", json=parameters)
                
                # GET requests
                elif any(api_route.startswith(route) for route in [
                    "/employees/details",
                    "/employees/all",
                    "/balance",
                    "/liability",
                    "/payrolls/next-date"
                ]):
                    response = await client.get(f"{FASTAPI_BASE_URL}{prefixed_route}", params=parameters)
                
                else:
                    raise HTTPException(status_code=400, detail=f"Unsupported API route: {api_route}")

                response.raise_for_status()
                return response.json()

        except httpx.HTTPError as e:
            logger.error(f"API call failed: {str(e)}")
            raise HTTPException(
                status_code=e.response.status_code if hasattr(e, 'response') else 500,
                detail=f"API call failed: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")