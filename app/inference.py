import logging
import json
import requests
import re
from datetime import datetime
from zoneinfo import ZoneInfo
import os
logger = logging.getLogger(__name__)


def run_redaction(id, input_text, model):
    """
    Run redaction on a prompt.
    """

    try:
        # Send post request to ollama chat endpoint
        response = requests.post(
            os.getenv("OLLAMA_CHAT_URL", "http://localhost:11434/api/chat"),
            json={
                "model": model,
                "messages": [
                    {"role": "user", 
                     "content": f"Input Text: {input_text}"}
                ],
                "stream": False
            }
        )
        
        # Convert to json 
        response = response.json()

        # Get the assistant's reply
        reply = response["message"]["content"]

        # Extract JSON from response
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", reply, re.DOTALL)
        
        if match:
            json_str = match.group(1)
            json_obj = json.loads(json_str)

            # Save metadata
            json_obj["id"] = str(id)  
            json_obj["total_duration_seconds"] = round(int(response["total_duration"]) / 1_000_000_000, 2)
            json_obj["model"] = response["model"]
            created_at_utc = response["created_at"]
            created_at_pacific = datetime.fromisoformat(created_at_utc).astimezone(ZoneInfo("America/Los_Angeles")).isoformat()
            json_obj["created_at"] = created_at_pacific

            return {
                "id": json_obj["id"],
                "redacted_text": json_obj["redacted_text"],
                "redacted_cases": json_obj["redacted_cases"],
                "model": json_obj["model"],
                "total_duration_seconds": json_obj["total_duration_seconds"],
                "created_at": json_obj["created_at"]
            }

    except Exception as e:
        print(e)

        