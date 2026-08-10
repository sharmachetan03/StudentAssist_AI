import logging
from typing import Dict, Any
from pydantic import ValidationError
from schema.models import UserQueryRequest

logger = logging.getLogger(__name__)


class ReceivingAgent:
    """
    Handles input ingestion, parsing, and validation for incoming student requests.
    """

    def process_input(self, raw_input: Dict[str, Any]) -> UserQueryRequest:
        """
        Parses raw dictionary payload into a validated UserQueryRequest Pydantic model.
        """
        logger.info("ReceivingAgent: Beginning payload validation...")
        
        if not raw_input:
            logger.error("ReceivingAgent: Received empty payload.")
            raise ValueError("Input payload cannot be empty.")

        try:
            # Extract nested context dict if present
            context = raw_input.get("context", {})

            # Extract user query across potential UI keys
            extracted_query = (
                raw_input.get("user_input") or 
                raw_input.get("query") or 
                raw_input.get("prompt") or 
                ""
            )

            # Map Streamlit UI payload fields to UserQueryRequest schema
            payload_data = {
                "student_id": context.get("name") or raw_input.get("student_id", "Student"),
                "query": extracted_query,
                "role": context.get("role", "Student"),
                "grade": context.get("grade", "Grade 5"),
                "curriculum": context.get("curriculum", "NCERT / CBSE"),
                "learning_style": context.get("learning_style", "Visual & Diagrammatic"),
                "history": raw_input.get("history", [])
            }

            # Validate payload against the Pydantic schema
            validated_request = UserQueryRequest(**payload_data)
            
            logger.info(
                f"ReceivingAgent: Successfully validated query for student "
                f"'{validated_request.student_id}'"
            )
            return validated_request

        except ValidationError as ve:
            logger.error(f"ReceivingAgent: Schema validation error:\n{ve.json()}")
            raise ve
        except Exception as e:
            logger.error(f"ReceivingAgent: Unexpected error during validation: {str(e)}")
            raise e