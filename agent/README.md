# Rika Smart Contract Client

A powerful Web3 client for interacting with Rika payroll smart contracts.

## Factory Contract Routes

### Create Payroll Contract

- **Route:** `POST /payroll-contracts`
- **Purpose:** Creates a new payroll contract for an employer
- **Parameters:** `employer_address`
- **Returns:** Transaction data with gas estimation

## Payroll Contract Routes

### Employee Management

- **Route:** `POST /employees`
- **Purpose:** Add a new employee to payroll
- **Parameters:** `name`, `employee_address`, `salary`, `employer_address`, `contract_index`

### Funds Management

- **Route:** `POST /funds`
- **Purpose:** Add funds to payroll contract
- **Parameters:** `amount`, `employer_address`, `contract_index`

### Schedule Management

- **Route:** `POST /schedules`
- **Purpose:** Create payment schedule for employee
- **Parameters:** `employee_address`, `start_date`, `end_date`, `interval`, `employer_address`, `contract_index`

### Employee Status

- **Route:** `POST /employees/deactivate`
- **Purpose:** Deactivate an employee
- **Parameters:** `employee_address`, `employer_address`, `contract_index`

- **Route:** `POST /employees/reactivate`
- **Purpose:** Reactivate an employee
- **Parameters:** `employee_address`, `employer_address`, `contract_index`

### Salary Updates

- **Route:** `POST /salaries/update`
- **Purpose:** Update employee salary
- **Parameters:** `employee_address`, `new_salary`, `employer_address`, `contract_index`

### Payroll Processing

- **Route:** `POST /payrolls/process`
- **Purpose:** Process all pending payrolls
- **Parameters:** `employer_address`, `contract_index`

### Information Retrieval

- **Route:** `GET /employees/details`
- **Purpose:** Get specific employee details
- **Parameters:** `employee_address`, `employer_address`, `contract_index`

- **Route:** `GET /employees/all`
- **Purpose:** Get all employees with details
- **Parameters:** `employer_address`, `contract_index`

- **Route:** `GET /balance`
- **Purpose:** Get employer's contract balance
- **Parameters:** `employer_address`, `contract_index`

- **Route:** `GET /liability`
- **Purpose:** Get total payroll liability
- **Parameters:** `employer_address`, `contract_index`

- **Route:** `GET /payrolls/next-date`
- **Purpose:** Get next payroll date for employee
- **Parameters:** `employee_address`, `employer_address`, `contract_index`

## Health Check

- **Route:** `GET /health`
- **Purpose:** Check API health status
- **Returns:** Version and status information

## AI Agent Integration

### Conversational Interface

- Natural language processing for payroll management
- Intelligent request interpretation and routing
- Context-aware responses and suggestions

### WebSocket Connection

- **Route:** `GET /ws/{employer_address}`
- **Purpose:** Real-time bidirectional communication
- **Features:**
    - Interactive chat interface
    - Transaction parameter collection
    - Guided workflow assistance

### HTTP Endpoint

- **Route:** `POST /agent/interact`
- **Purpose:** Single request-response interaction
- **Parameters:**
    - `prompt_text`: User's natural language input
    - `employer_address`: Ethereum address of employer
    - `session_id`: Optional session identifier

### Agent Capabilities

- Smart contract interaction guidance
- Parameter validation and collection
- Transaction preparation and explanation
- Error handling and recovery suggestions
- Contextual help and examples

### Response Format

```json
{
    "api_route": "Route selected for the operation",
    "parameters": "Extracted parameters for the operation",
    "error": "Error message if applicable",
    "api_response": "Response from the API call",
    "parameter_request": "Missing parameter details if needed",
    "session_id": "Session identifier",
    "help_buttons": "Interactive help options"
}
```

## Automated Tasks

### Celery Worker
- Scheduled payroll processing
- Transaction monitoring
- Error reporting
- Health checks

### Celery Beat Schedule

```json
{
    "process-payroll-daily": {
        "task": "agent.app.tasks.process_payroll_for_all_employers",
        "schedule": "0 0 * * *" // crontab(hour=0, minute=0) or a cron string
    }
}
```

## Architecture
- FastAPI for REST API endpoints
- WebSocket for real-time communication
- Celery for task scheduling
- Redis for message broker and result backend
- Web3.py for blockchain interactions
- Claude AI for natural language processing

## Security
- Private key management
- Transaction signing
- Rate limiting
- Input validation
- Error handling

## Contributing
- Fork the repository
- Create a feature branch
- Commit your changes
- Push to the branch
- Create a Pull Request

## License
- MIT License
