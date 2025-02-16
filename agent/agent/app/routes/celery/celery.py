from celery import Celery
from fastapi import APIRouter

router = APIRouter()

@router.post("/trigger-payroll-processing")
async def trigger_payroll_processing():
    """Trigger payroll processing for all employers."""
    from app.tasks.celery import process_payroll_for_all_employers
    task = process_payroll_for_all_employers.delay()
    return {"task_id": task.id, "status": "Payroll processing started."}