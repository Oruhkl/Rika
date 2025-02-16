from fastapi import FastAPI, HTTPException, APIRouter
from typing import List, Optional, Dict, Any
from app.routes.web3.model import  (BaseResponse, CreatePayrollContractRequest, AddEmployeeRequest, AddEmployeesBatchRequest, AddFundsRequest, CreateScheduleRequest, EmployeeStatusRequest, UpdateSalaryRequest, PayrollProcessRequest, GetDetailsRequest)
from app.contract.client import (create_payroll_contract, add_employee, add_employees_batch, add_funds, create_schedule, deactivate_employee, reactivate_employee, update_employee_salary, process_all_payrolls, get_employee_details, get_all_employees_with_details, get_employer_balance, get_total_payroll_liability, get_next_payroll_date, get_employer_payroll_contract)


router = APIRouter()


# --- Routes ---
@router.post("/payroll-contracts", response_model=BaseResponse)
async def create_payroll_contract_endpoint(request: CreatePayrollContractRequest):
    try:
        result = create_payroll_contract(request.employer_address)
        return BaseResponse(
            success=True,
            message="Operation successful",
            data=result,
            error=None
        )
    except Exception as e:
        return BaseResponse(
            success=False,
            message="Operation failed",
            data=None,
            error=str(e)
        )



@router.post("/employees", response_model=BaseResponse)
async def add_employee_endpoint(request: AddEmployeeRequest):
    try:
        result = add_employee(
            name=request.name,
            employee_address=request.employee_address,
            salary=request.salary,
            employer_address=request.employer_address,
            contract_index=request.contract_index
        )
        return BaseResponse(
            success=True,
            message="Operation successful",
            data=result,
            error=None
        )
    except Exception as e:
        return BaseResponse(
            success=False,
            message="Operation failed",
            data=None,
            error=str(e)
        )

@router.post("/funds", response_model=BaseResponse)
async def add_funds_endpoint(request: AddFundsRequest):
    try:
        result = add_funds(
            request.amount,
            request.employer_address,
            request.contract_index
        )
        return BaseResponse(
            success=True,
            message="Operation successful",
            data=result,
            error=None
        )
    except Exception as e:
        return BaseResponse(
            success=False,
            message="Operation failed",
            data=None,
            error=str(e)
        )

@router.post("/schedules", response_model=BaseResponse)
async def create_schedule(request: CreateScheduleRequest):
    try:
        result = create_schedule(
            request.employee_address,
            request.start_date,
            request.end_date,
            request.interval,
            request.employer_address,
            request.contract_index
        )
        return BaseResponse(success=True, message="Operation successful", data=result, error=None)
    except Exception as e:
        return BaseResponse(success=False, message="Operation failed", data=None, error=str(e))

@router.post("/employees/deactivate", response_model=BaseResponse)
async def deactivate_employee(request: EmployeeStatusRequest):
    try:
        result = deactivate_employee(
            request.employee_address,
            request.employer_address,
            request.contract_index
        )
        return BaseResponse(success=True, message="Operation successful", data=result, error=None)
    except Exception as e:
        return BaseResponse(success=False, message="Operation failed", data=None, error=str(e))

@router.post("/employees/reactivate", response_model=BaseResponse)
async def reactivate_employee(request: EmployeeStatusRequest):
    try:
        result = reactivate_employee(
            request.employee_address,
            request.employer_address,
            request.contract_index
        )
        return BaseResponse(success=True, message="Operation successful", data=result, error=None)
    except Exception as e:
        return BaseResponse(success=False, message="Operation failed", data=None, error=str(e))

@router.post("/salaries/update", response_model=BaseResponse)
async def update_salary(request: UpdateSalaryRequest):
    try:
        result = update_employee_salary(
            request.employee_address,
            request.new_salary,
            request.employer_address,
            request.contract_index
        )
        return BaseResponse(success=True, message="Operation successful", data=result, error=None)
    except Exception as e:
        return BaseResponse(success=False, message="Operation failed", data=None, error=str(e))

@router.post("/payrolls/process", response_model=BaseResponse)
async def process_payrolls(request: PayrollProcessRequest):
    try:
        result = process_all_payrolls(
            request.employer_address,
            request.contract_index
        )
        return BaseResponse(success=True, message="Operation successful", data=result, error=None)
    except Exception as e:
        return BaseResponse(success=False, message="Operation failed", data=None, error=str(e))

@router.get("/employees/details", response_model=BaseResponse)
async def get_employee_details(request: GetDetailsRequest):
    try:
        if not request.employee_address:
            raise ValueError("Employee address required")
        result = get_employee_details(
            request.employee_address,
            request.employer_address,
            request.contract_index
        )
        return BaseResponse(success=True, message="Operation successful", data=result, error=None)
    except Exception as e:
        return BaseResponse(success=False, message="Operation failed", data=None, error=str(e))

@router.get("/employees/all", response_model=BaseResponse)
async def get_all_employees(request: GetDetailsRequest):
    try:
        result = get_all_employees_with_details(
            request.employer_address,
            request.contract_index
        )
        return BaseResponse(success=True, message="Operation successful", data=result, error=None)
    except Exception as e:
        return BaseResponse(success=False, message="Operation failed", data=None, error=str(e))

@router.get("/balance", response_model=BaseResponse)
async def get_balance(request: GetDetailsRequest):
    try:
        result = get_employer_balance(
            request.employer_address,
            request.contract_index
        )
        return BaseResponse(success=True, message="Operation successful", data=result, error=None)
    except Exception as e:
        return BaseResponse(success=False, message="Operation failed", data=None, error=str(e))

@router.get("/liability", response_model=BaseResponse)
async def get_liability(request: GetDetailsRequest):
    try:
        result = get_total_payroll_liability(
            request.employer_address,
            request.contract_index
        )
        return BaseResponse(success=True, message="Operation successful", data=result, error=None)
    except Exception as e:
        return BaseResponse(success=False, message="Operation failed", data=None, error=str(e))

@router.get("/payrolls/next-date", response_model=BaseResponse)
async def get_next_date(request: GetDetailsRequest):
    try:
        if not request.employee_address:
            raise ValueError("Employee address required")
        result = get_next_payroll_date(
            request.employee_address,
            request.employer_address,
            request.contract_index
        )
        return BaseResponse(success=True, message="Operation successful", data=result, error=None)
    except Exception as e:
        return BaseResponse(success=False, message="Operation failed", data=None, error=str(e))


@router.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}




def get_router():
    return router