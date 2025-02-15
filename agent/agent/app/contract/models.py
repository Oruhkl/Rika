from pydantic import BaseModel, Field
from typing import List

class CreatePayrollContractInput(BaseModel):
    employer_address: str = Field(description="The EVM address of the employer.")

class AddEmployeeInput(BaseModel):
    name: str = Field(description="The name of the employee.")
    employee_address: str = Field(description="The EVM address of the employee.")
    salary: int = Field(description="The salary of the employee in the smallest unit (e.g., wei for ETH).")
    employer_address: str = Field(description="The EVM address of the employer.")

class AddEmployeesBatchInput(BaseModel):
    names: List[str] = Field(description="List of employee names.")
    employee_addresses: List[str] = Field(description="List of employee EVM addresses.")
    salaries: List[int] = Field(description="List of employee salaries in the smallest unit.")
    employer_address: str = Field(description="The EVM address of the employer.")

class AddFundsInput(BaseModel):
    amount: int = Field(description="The amount to add to the employer's balance in the smallest unit.")
    employer_address: str = Field(description="The EVM address of the employer.")

class CreateScheduleInput(BaseModel):
    employer_address: str = Field(description="The EVM address of the employer.")
    employee_address: str = Field(description="The EVM address of the employee.")
    start_date: int = Field(description="The start date of the schedule (Unix timestamp).")
    end_date: int = Field(description="The end date of the schedule (Unix timestamp).")
    interval: int = Field(description="The payment interval (e.g., 0 for weekly, 1 for biweekly, 2 for monthly).")

class DeactivateEmployeeInput(BaseModel):
    employee_address: str = Field(description="The EVM address of the employee to deactivate.")
    employer_address: str = Field(description="The EVM address of the employer.")

class ReactivateEmployeeInput(BaseModel):
    employee_address: str = Field(description="The EVM address of the employee to reactivate.")
    employer_address: str = Field(description="The EVM address of the employer.")

class UpdateEmployeeSalaryInput(BaseModel):
    employee_address: str = Field(description="The EVM address of the employee.")
    new_salary: int = Field(description="The new salary of the employee in the smallest unit.")
    employer_address: str = Field(description="The EVM address of the employer.")

class ProcessAllPayrollsInput(BaseModel):
    employer_address: str = Field(description="The EVM address of the employer.")

class GetEmployeeDetailsInput(BaseModel):
    employee_address: str = Field(description="The EVM address of the employee.")
    employer_address: str = Field(description="The EVM address of the employer.")

class GetAllEmployeesWithDetailsInput(BaseModel):
    employer_address: str = Field(description="The EVM address of the employer.")

class GetEmployerBalanceInput(BaseModel):
    employer_address: str = Field(description="The EVM address of the employer.")

class GetTotalPayrollLiabilityInput(BaseModel):
    employer_address: str = Field(description="The EVM address of the employer.")

class HasSufficientBalanceForPayrollInput(BaseModel):
    employer_address: str = Field(description="The EVM address of the employer.")

class GetNextPayrollDateInput(BaseModel):
    employee_address: str = Field(description="The EVM address of the employee.")
    employer_address: str = Field(description="The EVM address of the employer.")
