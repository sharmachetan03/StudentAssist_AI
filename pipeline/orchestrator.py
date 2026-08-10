import logging
from typing import Dict, Any
from agents.receiving_agent import ReceivingAgent
from agents.ar_agent import ARAgent

logger = logging.getLogger(__name__)


class PipelineOrchestrator:

    def __init__(self):
        logger.info("🚀 Initializing Pipeline Orchestrator...")
        self.receiving_agent = ReceivingAgent()
        self.ar_agent = ARAgent()

    def _format_conversation_history(self, history: list) -> str:
        """Formats prior chat messages into a clean block for the LLM context."""
        if not history:
            return ""

        formatted_turns = []
        for msg in history:
            role = "User" if msg.get("role") == "user" else "Assistant"
            content = msg.get("content", "").strip()
            # Clean diagram clutter from history memory buffer
            if "```mermaid" in content:
                content = content.split("```mermaid")[0] + "[Diagram Generated]"
            formatted_turns.append(f"{role}: {content}")

        history_text = "\n".join(formatted_turns)
        return f"\n\n--- PREVIOUS CONVERSATION HISTORY ---\n{history_text}\n-----------------------------------\n"

    def _inject_formatting_instructions(self, validated_request: Any) -> Any:
        """
        Injects explicit rules to prevent squished text, broken LaTeX blocks, 
        and invalid single-line Mermaid syntax.
        """
        formatting_addon = (
            "\n\n[STRICT FORMATTING & LATEX RULES]:\n"
            "1. ALWAYS separate headings (##), bullet points (*), and paragraphs with DOUBLE NEWLINES (\\n\\n). Do NOT compress multiple sections into a single line.\n"
            "2. If writing multi-line math or division steps, use standard display math blocks cleanly wrapped in double dollar signs:\n"
            "   $$\n"             "   \\begin{aligned}\n"             "   36 \\div 2 &= 18 \\\\\n"             "   18 \\div 2 &= 9\n"             "   \\end{aligned}\n"             "   $$\n"
            "3. Do NOT output orphaned \\end{aligned} tags without an opening \\begin{aligned}.\n"
            "4. For Mermaid diagrams, always use valid multi-line syntax inside ```mermaid code blocks.\n"
        )

        if hasattr(validated_request, "query"):
            validated_request.query += formatting_addon

        return validated_request

    def process_query(self, validated_request, history: list = None):
        """Processes query through ARAgent with formatted history and strict layout instructions."""
        logger.info(
            f"Dispatching query for Student ID: {getattr(validated_request, 'student_id', 'N/A')}"
        )

        # 1. Attach formatted conversation history to query
        if history and hasattr(validated_request, "query"):
            history_context = self._format_conversation_history(history)
            validated_request.query = f"{history_context}\nCURRENT USER QUERY: {validated_request.query}"

        # 2. Inject strict formatting and LaTeX rules
        validated_request = self._inject_formatting_instructions(validated_request)

        # 3. Delegate execution to ARAgent
        ar_response = self.ar_agent.generate_response(validated_request)
        return ar_response

    def run_pipeline(self, raw_input: Dict[str, Any]):
        """Runs the complete end-to-end pipeline flow."""
        try:
            raw_history = raw_input.get("history", [])
            validated_request = self.receiving_agent.process_input(raw_input)
            ar_response = self.process_query(validated_request, history=raw_history)
            return ar_response

        except Exception as e:
            logger.error(f"Pipeline execution failed: {str(e)}")
            raise e

    def process(self, raw_input: Dict[str, Any]):
        """Alias for run_pipeline for backward compatibility."""
        return self.run_pipeline(raw_input)