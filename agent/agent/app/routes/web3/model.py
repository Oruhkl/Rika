from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# --- Schema Definitions ---
class BaseResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class CreatePayrollContractRequest(BaseModel):
    employer_address: str

class AddEmployeeRequest(BaseModel):
    name: str
    employee_address: str
    salary: int
    employer_address: str
    contract_index: int = 0

class AddEmployeesBatchRequest(BaseModel):
    names: List[str]
    employee_addresses: List[str]
    salaries: List[int]
    employer_address: str
    contract_index: int = 0

class AddFundsRequest(BaseModel):
    amount: int
    employer_address: str
    contract_index: int = 0

class CreateScheduleRequest(BaseModel):
    employee_address: str
    start_date: int
    end_date: int
    interval: int
    employer_address: str
    contract_index: int = 0

class EmployeeStatusRequest(BaseModel):
    employee_address: str
    employer_address: str
    contract_index: int = 0

class UpdateSalaryRequest(BaseModel):
    employee_address: str
    new_salary: int
    employer_address: str
    contract_index: int = 0

class PayrollProcessRequest(BaseModel):
    employer_address: str
    contract_index: int = 0

class GetDetailsRequest(BaseModel):
    employer_address: str
    contract_index: int = 0
    employee_address: Optional[str] = None
