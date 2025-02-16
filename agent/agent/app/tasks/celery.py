from celery import Celery
from celery.schedules import crontab
from app.contract.client import get_all_payroll_contracts_with_employers, process_all_payrolls
from web3 import Web3
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Web3 and wallet setup
w3 = Web3(Web3.HTTPProvider(os.getenv('WEB3_PROVIDER_URI')))
AGENT_WALLET_ADDRESS = os.getenv("AGENT_WALLET_ADDRESS")
AGENT_PRIVATE_KEY = os.getenv("AGENT_PRIVATE_KEY")

celery_app = Celery(
    "rika_worker",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
)

celery_app.conf.update(
    result_expires=3600,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@celery_app.task
def process_payroll_for_all_employers():
    """Celery task to process payroll for all employers and their contracts."""
    try:
        result = get_all_payroll_contracts_with_employers()
        if "error" in result:
            raise Exception(result["error"])
            
        employers = result["employers"]
        contracts = result["contracts"]
        
        for employer, contract in zip(employers, contracts):
            # Get the transaction data
            process_result = process_all_payrolls(employer)
            
            if "transaction" in process_result:
                # Sign and send transaction
                signed_txn = w3.eth.account.sign_transaction(
                    process_result["transaction"],
                    private_key=AGENT_PRIVATE_KEY
                )
                
                # Send the signed transaction
                tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
                
                # Wait for transaction receipt
                tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
                
                logger.info(f"Processed payroll for employer {employer}: TX Hash {tx_hash.hex()}")
            else:
                logger.error(f"No transaction data for employer {employer}")
        
        return {"status": "success", "message": "Payroll processing completed for all employers."}
    except Exception as e:
        logger.error(f"Error processing payroll: {e}")
        return {"status": "error", "message": str(e)}
