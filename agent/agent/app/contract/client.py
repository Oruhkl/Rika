import os
from dotenv import load_dotenv
from web3 import Web3
from web3.exceptions import ContractLogicError
from typing import List, Dict, Any
from app.contract.abi import RIKA_FACTORY_ABI, RIKA_MANAGEMENT_ABI
from app.contract.models import (
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
        try:
            # Try estimation first
            estimated_gas = rika_factory.functions.createPayrollContract().estimate_gas(params)
            params['gas'] = estimated_gas + 150000  # Buffer for safety
        except:
            # Fall back to fixed gas if estimation fails
            params['gas'] = 300000
            
        tx = rika_factory.functions.createPayrollContract().build_transaction(params)
        return {
            "transaction": tx,
            "message": "Transaction built successfully",
            "gas_estimation": "dynamic" if 'estimated_gas' in locals() else "fixed"
        }
    except ContractLogicError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}
def get_employer_payroll_contract(employer_address: str, contract_index: int = 0) -> Dict[str, Any]:
    """Gets specific payroll contract instance based on index."""
    try:
        contracts = rika_factory.functions.getEmployerPayrolls(employer_address).call({'from': employer_address})
        
        if not contracts:
            return {"error": "No payroll contracts found"}
            
        if contract_index >= len(contracts):
            return {"error": f"Invalid contract index. Max index is {len(contracts)-1}"}
            
        selected_contract = w3.eth.contract(
            address=contracts[contract_index],
            abi=RIKA_MANAGEMENT_ABI
        )
        
        return {
            "all_contracts": contracts,
            "selected_contract": selected_contract,
            "selected_address": contracts[contract_index],
            "message": f"Using payroll contract {contract_index+1} of {len(contracts)}"
        }
        
    except ContractLogicError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

# Rika Management Functions
def get_contract_instance(employer_address: str, contract_index: int = 0) -> Dict[str, Any]:
    """Gets the appropriate contract instance."""
    try:
        contracts = rika_factory.functions.getEmployerPayrolls(employer_address).call({'from': employer_address})
        if not contracts:
            return {"error": "No payroll contracts found"}
        if contract_index >= len(contracts):
            return {"error": f"Invalid contract index. Max index is {len(contracts)-1}"}
            
        return w3.eth.contract(address=contracts[contract_index], abi=RIKA_MANAGEMENT_ABI)
    except Exception as e:
        return {"error": str(e)}

def add_employee(name: str, employee_address: str, salary: int, employer_address: str, contract_index: int = 0) -> Dict[str, Any]:
    """Adds a new employee. Returns unsigned transaction."""
    try:
        contract = get_contract_instance(employer_address, contract_index)
        if "error" in contract:
            return contract
            
        params = build_transaction_params(employer_address)
        params['gas'] = contract.functions.addEmployee(name, employee_address, salary).estimate_gas(params) + 100000
        tx = contract.functions.addEmployee(name, employee_address, salary).build_transaction(params)
        return {"transaction": tx, "message": "Transaction built successfully"}
    except ContractLogicError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

def add_employees_batch(names: List[str], employee_addresses: List[str], salaries: List[int], employer_address: str, contract_index: int = 0) -> Dict[str, Any]:
    """Adds multiple employees. Returns unsigned transaction."""
    try:
        contract = get_contract_instance(employer_address, contract_index)
        if "error" in contract:
            return contract
            
        params = build_transaction_params(employer_address)
        params['gas'] = contract.functions.addEmployeesBatch(names, employee_addresses, salaries).estimate_gas(params) + 200000
        tx = contract.functions.addEmployeesBatch(names, employee_addresses, salaries).build_transaction(params)
        return {"transaction": tx, "message": "Transaction built successfully"}
    except ContractLogicError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}
def add_funds(amount: int, employer_address: str, contract_index: int = 0) -> Dict[str, Any]:
    """Adds funds to the payroll contract. Returns unsigned transaction."""
    try:
        contract = get_contract_instance(employer_address, contract_index)
        if "error" in contract:
            return contract
            
        params = build_transaction_params(employer_address)
        params['gas'] = contract.functions.addFunds(amount).estimate_gas(params) + 100000
        tx = contract.functions.addFunds(amount).build_transaction(params)
        return {"transaction": tx, "message": "Transaction built successfully"}
    except ContractLogicError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

def create_schedule(employee_address: str, start_date: int, end_date: int, interval: int, employer_address: str, contract_index: int = 0) -> Dict[str, Any]:
    """Creates a payroll schedule. Returns unsigned transaction."""
    try:
        contract = get_contract_instance(employer_address, contract_index)
        if "error" in contract:
            return contract
            
        params = build_transaction_params(employer_address)
        params['gas'] = contract.functions.createSchedule(employee_address, start_date, end_date, interval).estimate_gas(params) + 150000
        tx = contract.functions.createSchedule(employee_address, start_date, end_date, interval).build_transaction(params)
        return {"transaction": tx, "message": "Transaction built successfully"}
    except ContractLogicError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

def deactivate_employee(employee_address: str, employer_address: str, contract_index: int = 0) -> Dict[str, Any]:
    """Deactivates an employee. Returns unsigned transaction."""
    try:
        contract = get_contract_instance(employer_address, contract_index)
        if "error" in contract:
            return contract
            
        params = build_transaction_params(employer_address)
        params['gas'] = contract.functions.deactivateEmployee(employee_address).estimate_gas(params) + 100000
        tx = contract.functions.deactivateEmployee(employee_address).build_transaction(params)
        return {"transaction": tx, "message": "Transaction built successfully"}
    except ContractLogicError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

def reactivate_employee(employee_address: str, employer_address: str, contract_index: int = 0) -> Dict[str, Any]:
    """Reactivates an employee. Returns unsigned transaction."""
    try:
        contract = get_contract_instance(employer_address, contract_index)
        if "error" in contract:
            return contract
            
        params = build_transaction_params(employer_address)
        params['gas'] = contract.functions.reactivateEmployee(employee_address).estimate_gas(params) + 100000
        tx = contract.functions.reactivateEmployee(employee_address).build_transaction(params)
        return {"transaction": tx, "message": "Transaction built successfully"}
    except ContractLogicError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

def update_employee_salary(employee_address: str, new_salary: int, employer_address: str, contract_index: int = 0) -> Dict[str, Any]:
    """Updates an employee's salary. Returns unsigned transaction."""
    try:
        contract = get_contract_instance(employer_address, contract_index)
        if "error" in contract:
            return contract
            
        params = build_transaction_params(employer_address)
        params['gas'] = contract.functions.updateEmployeeSalary(employee_address, new_salary).estimate_gas(params) + 100000
        tx = contract.functions.updateEmployeeSalary(employee_address, new_salary).build_transaction(params)
        return {"transaction": tx, "message": "Transaction built successfully"}
    except ContractLogicError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

def process_all_payrolls(employer_address: str, contract_index: int = 0) -> Dict[str, Any]:
    """Processes all payrolls. Returns unsigned transaction."""
    try:
        contract = get_contract_instance(employer_address, contract_index)
        if "error" in contract:
            return contract
            
        params = build_transaction_params(employer_address)
        params['gas'] = contract.functions.processAllPayrolls().estimate_gas(params) + 200000
        tx = contract.functions.processAllPayrolls().build_transaction(params)
        return {"transaction": tx, "message": "Transaction built successfully"}
    except ContractLogicError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}
def get_contract_instance(employer_address: str, contract_index: int = 0) -> Dict[str, Any]:
    """Gets the appropriate contract instance."""
    try:
        contracts = rika_factory.functions.getEmployerPayrolls(employer_address).call({'from': employer_address})
        if not contracts:
            return {"error": "No payroll contracts found"}
        if contract_index >= len(contracts):
            return {"error": f"Invalid contract index. Max index is {len(contracts)-1}"}
            
        return w3.eth.contract(address=contracts[contract_index], abi=RIKA_MANAGEMENT_ABI)
    except Exception as e:
        return {"error": str(e)}

def add_employee(name: str, employee_address: str, salary: int, employer_address: str, contract_index: int = 0) -> Dict[str, Any]:
    """Adds a new employee. Returns unsigned transaction."""
    try:
        contract = get_contract_instance(employer_address, contract_index)
        if "error" in contract:
            return contract
            
        params = build_transaction_params(employer_address)
        params['gas'] = contract.functions.addEmployee(name, employee_address, salary).estimate_gas(params) + 100000
        tx = contract.functions.addEmployee(name, employee_address, salary).build_transaction(params)
        return {"transaction": tx, "message": "Transaction built successfully"}
    except ContractLogicError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

def add_employees_batch(names: List[str], employee_addresses: List[str], salaries: List[int], employer_address: str, contract_index: int = 0) -> Dict[str, Any]:
    """Adds multiple employees. Returns unsigned transaction."""
    try:
        contract = get_contract_instance(employer_address, contract_index)
        if "error" in contract:
            return contract
            
        params = build_transaction_params(employer_address)
        params['gas'] = contract.functions.addEmployeesBatch(names, employee_addresses, salaries).estimate_gas(params) + 200000
        tx = contract.functions.addEmployeesBatch(names, employee_addresses, salaries).build_transaction(params)
        return {"transaction": tx, "message": "Transaction built successfully"}
    except ContractLogicError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}
def get_employee_details(employee_address: str, employer_address: str, contract_index: int = 0) -> Dict[str, Any]:
    """Retrieves detailed information about a specific employee."""
    try:
        contract = get_contract_instance(employer_address, contract_index)
        if "error" in contract:
            return contract
            
        details = contract.functions.getEmployeeDetails(employer_address, employee_address).call({'from': employer_address})
        return {"details": details, "message": "Successfully retrieved employee details"}
    except ContractLogicError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

def get_all_employees_with_details(employer_address: str, contract_index: int = 0) -> Dict[str, Any]:
    """Retrieves detailed information for all employees."""
    try:
        contract = get_contract_instance(employer_address, contract_index)
        if "error" in contract:
            return contract
            
        details = contract.functions.getAllEmployeesWithDetails(employer_address).call({'from': employer_address})
        return {"details": details, "message": "Successfully retrieved all employees"}
    except ContractLogicError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

def get_employer_balance(employer_address: str, contract_index: int = 0) -> Dict[str, Any]:
    """Retrieves the employer's payroll contract balance."""
    try:
        contract = get_contract_instance(employer_address, contract_index)
        if "error" in contract:
            return contract
            
        balance = contract.functions.getEmployerBalance(employer_address).call({'from': employer_address})
        return {"balance": balance, "message": "Successfully retrieved balance"}
    except ContractLogicError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

def get_total_payroll_liability(employer_address: str, contract_index: int = 0) -> Dict[str, Any]:
    """Calculates and retrieves the total payroll liability."""
    try:
        contract = get_contract_instance(employer_address, contract_index)
        if "error" in contract:
            return contract
            
        liability = contract.functions.getTotalPayrollLiability(employer_address).call({'from': employer_address})
        return {"liability": liability, "message": "Successfully retrieved liability"}
    except ContractLogicError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

def has_sufficient_balance_for_payroll(employer_address: str, contract_index: int = 0) -> Dict[str, Any]:
    """Checks if the employer has sufficient balance for payroll."""
    try:
        contract = get_contract_instance(employer_address, contract_index)
        if "error" in contract:
            return contract
            
        result = contract.functions.hasSufficientBalanceForPayroll(employer_address).call({'from': employer_address})
        return {"has_sufficient": result, "message": "Successfully checked balance"}
    except ContractLogicError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

def get_next_payroll_date(employee_address: str, employer_address: str, contract_index: int = 0) -> Dict[str, Any]:
    """Retrieves next payroll date."""
    try:
        contract = get_contract_instance(employer_address, contract_index)
        if "error" in contract:
            return contract
            
        date = contract.functions.getNextPayrollDate(employer_address, employee_address).call({'from': employer_address})
        return {"next_date": date, "message": "Successfully retrieved next payroll date"}
    except ContractLogicError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}
