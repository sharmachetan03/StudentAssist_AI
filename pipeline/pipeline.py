import logging
from agents.receiving_agent import ReceivingAgent
from agents.ar_agent import ARAgent

logger = logging.getLogger(__name__)

class StudentAssistPipeline:
    """
    Orchestrates the flow between ReceivingAgent and ARAgent.
    """
    def __init__(self):
        self.receiving_agent = ReceivingAgent()
        self.ar_agent = ARAgent()

    def run(self, raw_input: dict) -> str:
        # 1. Ingest and validate using ReceivingAgent
        request_data = self.receiving_agent.process_input(raw_input)
        
        # 2. Pass validated request to ARAgent (Gemini 3.6)
        response_data = self.ar_agent.generate_response(
            query=request_data.query,
            grade_level=request_data.student.grade_level,
            subject=request_data.subject
        )
        
        # 3. Return JSON output using Pydantic's serialization
        return response_data.model_dump_json(indent=2)