import os
from dotenv import load_dotenv
from web3 import Web3
from web3.exceptions import ContractLogicError
from typing import List, Dict, Any
from app.abi import RIKA_FACTORY_ABI, RIKA_MANAGEMENT_ABI
from langchain.tools import StructuredTool
from app.models import (
    CreatePayrollContractInput, AddEmployeeInput, AddEmployeesBatchInput, AddFundsInput,
    CreateScheduleInput, DeactivateEmployeeInput, ReactivateEmployeeInput,
    UpdateEmployeeSalaryInput, ProcessAllPayrollsInput, GetEmployeeDetailsInput,
    GetAllEmployeesWithDetailsInput, GetEmployerBalanceInput, GetTotalPayrollLiabilityInput,
    HasSufficientBalanceForPayrollInput, GetNextPayrollDateInput
)

load_dotenv()

# Connect to EVM node
w3 = Web3(Web3.HTTPProvider(os.getenv('WEB3_PROVIDER_URI')))

# Contract addresses
RIKA_FACTORY_CONTRACT_ADDRESS = os.getenv('RIKA_FACTORY_CONTRACT_ADDRESS')
RIKA_MANAGEMENT_CONTRACT_ADDRESS = os.getenv('RIKA_MANAGEMENT_CONTRACT_ADDRESS')

# Initialize contracts
rika_factory = w3.eth.contract(
    address=RIKA_FACTORY_CONTRACT_ADDRESS,
    abi=RIKA_FACTORY_ABI
)

rika_management = w3.eth.contract(
    address=RIKA_MANAGEMENT_CONTRACT_ADDRESS,
    abi=RIKA_MANAGEMENT_ABI
)

def build_transaction_params(employer_address: str) -> Dict[str, Any]:
    """Build transaction parameters."""
    params = {
        'from': employer_address,
        'nonce': w3.eth.get_transaction_count(employer_address),
        'gasPrice': w3.eth.gas_price
    }
    return params

# Rika Factory Functions
def create_payroll_contract(employer_address: str) -> Dict[str, Any]:
    """Creates a new payroll contract. Returns unsigned transaction."""
    try:
        params = build_transaction_params(employer_address)
        params['gas'] = rika_factory.functions.createPayrollContract().estimate_gas(params) + 150000
        tx = rika_factory.functions.createPayrollContract().build_transaction(params)
        return {"transaction": tx, "message": "Transaction built successfully"}
    except ContractLogicError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

# Rika Management Functions
def add_employee(name: str, employee_address: str, salary: int, employer_address: str) -> Dict[str, Any]:
    """Adds a new employee. Returns unsigned transaction."""
    try:
        params = build_transaction_params(employer_address)
        params['gas'] = rika_management.functions.addEmployee(name, employee_address, salary).estimate_gas(params) + 100000
        tx = rika_management.functions.addEmployee(name, employee_address, salary).build_transaction(params)
        return {"transaction": tx, "message": "Transaction built successfully"}
    except ContractLogicError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

def add_employees_batch(names: List[str], employee_addresses: List[str], salaries: List[int], employer_address: str) -> Dict[str, Any]:
    """Adds multiple employees. Returns unsigned transaction."""
    try:
        params = build_transaction_params(employer_address)
        params['gas'] = rika_management.functions.addEmployeesBatch(names, employee_addresses, salaries).estimate_gas(params) + 200000
        tx = rika_management.functions.addEmployeesBatch(names, employee_addresses, salaries).build_transaction(params)
        return {"transaction": tx, "message": "Transaction built successfully"}
    except ContractLogicError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

def add_funds(amount: int, employer_address: str) -> Dict[str, Any]:
    """Adds funds to the payroll contract. Returns unsigned transaction."""
    try:
        params = build_transaction_params(employer_address)
        params['gas'] = rika_management.functions.addFunds(amount).estimate_gas(params) + 100000
        tx = rika_management.functions.addFunds(amount).build_transaction(params)
        return {"transaction": tx, "message": "Transaction built successfully"}
    except ContractLogicError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

def create_schedule(employee_address: str, start_date: int, end_date: int, interval: int, employer_address: str) -> Dict[str, Any]:
    """Creates a payroll schedule. Returns unsigned transaction."""
    try:
        params = build_transaction_params(employer_address)
        params['gas'] = rika_management.functions.createSchedule(employee_address, start_date, end_date, interval).estimate_gas(params) + 150000
        tx = rika_management.functions.createSchedule(employee_address, start_date, end_date, interval).build_transaction(params)
        return {"transaction": tx, "message": "Transaction built successfully"}
    except ContractLogicError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

def deactivate_employee(employee_address: str, employer_address: str) -> Dict[str, Any]:
    """Deactivates an employee. Returns unsigned transaction."""
    try:
        params = build_transaction_params(employer_address)
        params['gas'] = rika_management.functions.deactivateEmployee(employee_address).estimate_gas(params) + 100000
        tx = rika_management.functions.deactivateEmployee(employee_address).build_transaction(params)
        return {"transaction": tx, "message": "Transaction built successfully"}
    except ContractLogicError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

def reactivate_employee(employee_address: str, employer_address: str) -> Dict[str, Any]:
    """Reactivates an employee. Returns unsigned transaction."""
    try:
        params = build_transaction_params(employer_address)
        params['gas'] = rika_management.functions.reactivateEmployee(employee_address).estimate_gas(params) + 100000
        tx = rika_management.functions.reactivateEmployee(employee_address).build_transaction(params)
        return {"transaction": tx, "message": "Transaction built successfully"}
    except ContractLogicError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

def update_employee_salary(employee_address: str, new_salary: int, employer_address: str) -> Dict[str, Any]:
    """Updates an employee's salary. Returns unsigned transaction."""
    try:
        params = build_transaction_params(employer_address)
        params['gas'] = rika_management.functions.updateEmployeeSalary(employee_address, new_salary).estimate_gas(params) + 100000
        tx = rika_management.functions.updateEmployeeSalary(employee_address, new_salary).build_transaction(params)
        return {"transaction": tx, "message": "Transaction built successfully"}
    except ContractLogicError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

def process_all_payrolls(employer_address: str) -> Dict[str, Any]:
    """Processes all payrolls. Returns unsigned transaction."""
    try:
        params = build_transaction_params(employer_address)
        params['gas'] = rika_management.functions.processAllPayrolls().estimate_gas(params) + 200000
        tx = rika_management.functions.processAllPayrolls().build_transaction(params)
        return {"transaction": tx, "message": "Transaction built successfully"}
    except ContractLogicError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

def get_employee_details(employee_address: str, employer_address: str) -> str:
    """Retrieves detailed information about a specific employee."""
    try:
        details = rika_management.functions.getEmployeeDetails(employer_address, employee_address).call({'from': employer_address})
        return f"Employee details: {details}"
    except ContractLogicError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

def get_all_employees_with_details(employer_address: str) -> str:
    """Retrieves detailed information for all employees."""
    try:
        details = rika_management.functions.getAllEmployeesWithDetails(employer_address).call({'from': employer_address})
        return f"Employees details: {details}"
    except ContractLogicError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

def get_employer_balance(employer_address: str) -> str:
    """Retrieves the employer's payroll contract balance."""
    try:
        balance = rika_management.functions.getEmployerBalance(employer_address).call({'from': employer_address})
        return f"Balance: {balance}"
    except ContractLogicError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

def get_total_payroll_liability(employer_address: str) -> str:
    """Calculates and retrieves the total payroll liability."""
    try:
        liability = rika_management.functions.getTotalPayrollLiability(employer_address).call({'from': employer_address})
        return f"Total liability: {liability}"
    except ContractLogicError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

def has_sufficient_balance_for_payroll(employer_address: str) -> str:
    """Checks if the employer has sufficient balance for payroll."""
    try:
        result = rika_management.functions.hasSufficientBalanceForPayroll(employer_address).call({'from': employer_address})
        return f"Sufficient balance: {result}"
    except ContractLogicError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

def get_next_payroll_date(employee_address: str, employer_address: str) -> str:
    """Retrieves next payroll date."""
    try:
        date = rika_management.functions.getNextPayrollDate(employer_address, employee_address).call({'from': employer_address})
        return f"Next payroll date: {date}"
    except ContractLogicError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

# Structured Tools
create_payroll_contract_tool = StructuredTool(
    name="create_payroll_contract",
    description="Creates a new payroll contract. Returns unsigned transaction.",
    func=create_payroll_contract,
    args_schema=CreatePayrollContractInput,
    tags=["custom"]
)

add_employee_tool = StructuredTool(
    name="add_employee",
    description="Adds a new employee. Returns unsigned transaction.",
    func=add_employee,
    args_schema=AddEmployeeInput,
    tags=["custom"]
)

add_employees_batch_tool = StructuredTool(
    name="add_employees_batch",
    description="Adds multiple employees. Returns unsigned transaction.",
    func=add_employees_batch,
    args_schema=AddEmployeesBatchInput,
    tags=["custom"]
)

add_funds_tool = StructuredTool(
    name="add_funds",
    description="Adds funds to the payroll contract. Returns unsigned transaction.",
    func=add_funds,
    args_schema=AddFundsInput,
    tags=["custom"]
)

create_schedule_tool = StructuredTool(
    name="create_schedule",
    description="Creates a payroll schedule. Returns unsigned transaction.",
    func=create_schedule,
    args_schema=CreateScheduleInput,
    tags=["custom"]
)

deactivate_employee_tool = StructuredTool(
    name="deactivate_employee",
    description="Deactivates an employee. Returns unsigned transaction.",
    func=deactivate_employee,
    args_schema=DeactivateEmployeeInput,
    tags=["custom"]
)

reactivate_employee_tool = StructuredTool(
    name="reactivate_employee",
    description="Reactivates an employee. Returns unsigned transaction.",
    func=reactivate_employee,
    args_schema=ReactivateEmployeeInput,
    tags=["custom"]
)

update_employee_salary_tool = StructuredTool(
    name="update_employee_salary",
    description="Updates an employee's salary. Returns unsigned transaction.",
    func=update_employee_salary,
    args_schema=UpdateEmployeeSalaryInput,
    tags=["custom"]
)

process_all_payrolls_tool = StructuredTool(
    name="process_all_payrolls",
    description="Processes all payrolls. Returns unsigned transaction.",
    func=process_all_payrolls,
    args_schema=ProcessAllPayrollsInput,
    tags=["custom"]
)

get_employee_details_tool = StructuredTool(
    name="get_employee_details",
    description="Retrieves detailed information about a specific employee.",
    func=get_employee_details,
    args_schema=GetEmployeeDetailsInput,
    tags=["custom"]
)

get_all_employees_with_details_tool = StructuredTool(
    name="get_all_employees_with_details",
    description="Retrieves detailed information for all employees.",
    func=get_all_employees_with_details,
    args_schema=GetAllEmployeesWithDetailsInput,
    tags=["custom"]
)

get_employer_balance_tool = StructuredTool(
    name="get_employer_balance",
    description="Retrieves the employer's payroll contract balance.",
    func=get_employer_balance,
    args_schema=GetEmployerBalanceInput,
    tags=["custom"]
)

get_total_payroll_liability_tool = StructuredTool(
    name="get_total_payroll_liability",
    description="Calculates and retrieves the total payroll liability.",
    func=get_total_payroll_liability,
    args_schema=GetTotalPayrollLiabilityInput,
    tags=["custom"]
)

has_sufficient_balance_for_payroll_tool = StructuredTool(
    name="has_sufficient_balance_for_payroll",
    description="Checks if the employer has sufficient balance for payroll.",
    func=has_sufficient_balance_for_payroll,
    args_schema=HasSufficientBalanceForPayrollInput,
    tags=["custom"]
)

get_next_payroll_date_tool = StructuredTool(
    name="get_next_payroll_date",
    description="Retrieves next payroll date.",
    func=get_next_payroll_date,
    args_schema=GetNextPayrollDateInput,
    tags=["custom"]
)

# Export all tools in a list
TOOLS = [
    create_payroll_contract_tool,
    add_employee_tool,
    add_employees_batch_tool,
    add_funds_tool,
    create_schedule_tool,
    deactivate_employee_tool,
    reactivate_employee_tool,
    update_employee_salary_tool,
    process_all_payrolls_tool,
    get_employee_details_tool,
    get_all_employees_with_details_tool,
    get_employer_balance_tool,
    get_total_payroll_liability_tool,
    has_sufficient_balance_for_payroll_tool,
    get_next_payroll_date_tool
]