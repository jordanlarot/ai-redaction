from fastapi import FastAPI
from sqlalchemy.orm import Session
from database.models import RedactionRecord  # Ensure this matches your model
import logging
from typing import Union
from .schemas import RedactionRequest, RedactionResponse
from .inference import run_redaction
from .database import SessionLocal

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize the FastAPI app
app = FastAPI()


@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "Redaction API is running."}


# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}


# Redaction endpoint
@app.post("/redact", response_model=RedactionResponse)
def chat(request: RedactionRequest):

    logger.info(f"Redaction request received with id={request.id}, model={request.model}")

    try:
        result = run_redaction(
            id=request.id,
            input_text=request.input_text,
            model=request.model,
        )
        
        logger.info("Redaction run completed successfully")

        if request.add_to_db:
            db: Session = SessionLocal()

            # Create a new record to store the redacted data
            new_record = RedactionRecord(
                id=result["id"],
                redacted_text=result["redacted_text"],
                redacted_cases=result["redacted_cases"],
                total_duration_seconds=result["total_duration_seconds"],
                created_at=result["created_at"],
                model=result["model"],
            )

            # Add and commit the record to the database
            db.add(new_record)
            db.commit()
            db.refresh(new_record)

            logger.info("Added to database successfully")

            # Ensure the session is closed
            db.close()  

        return RedactionResponse(
            id=result["id"],
            redacted_text=result["redacted_text"],
            redacted_cases=result["redacted_cases"],
            total_duration_seconds=result["total_duration_seconds"],
            created_at=result["created_at"],
            model=result["model"],
        )
    
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}", exc_info=True)
        raise
