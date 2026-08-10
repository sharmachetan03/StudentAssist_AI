import sys
from pathlib import Path

# Ensure root project directory is in system path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from pipeline.orchestrator import PipelineOrchestrator


def main():
    # Payload matching the flattened UserQueryRequest schema (Option A)
    payload = {
        "student_id": "STU12345",
        "subject": "Science",
        "query": "Explain how photosynthesis works in simple terms.",
        "metadata": {
            "session_id": "SESS_9988",
            "timestamp": "2026-08-04T10:00:00Z",
            "grade": 8
        }
    }

    print("🚀 Initializing Pipeline Orchestrator...")
    orchestrator = PipelineOrchestrator()

    print("🔄 Processing input payload through agent pipeline...")
    result = orchestrator.run_pipeline(payload)

    print("\n✅ Pipeline Executed Successfully!")
    print("-----------------------------------")
    print(result)


if __name__ == "__main__":
    main()