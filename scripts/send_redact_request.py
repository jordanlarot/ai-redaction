import requests
import json


def send_redact_request(id, input_text, model, add_to_db=False):
    """
    Send a redaction request to the /redact endpoint.

    Args:
        id (int): The id of the input text.
        input_text (str): The input text to be redacted.
        model (str): The model to use for redaction.
        add_to_db (bool): Whether to add the redaction record to the database.
    """

    try:
        json_response = requests.post(
            "http://127.0.0.1:8000/redact", 
            json={
            "id": str(id),
            "input_text": input_text,
            "model": model,
            "add_to_db": add_to_db
        }
    )
        # Convert the response to a json object
        json_obj = json_response.json()

        return json_obj

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":

    # Send a redaction request
    response = send_redact_request(1, 
                                   "My name is John Doe and I live in New York City.", 
                                   "redaction:4b")

    # Print out the response
    print(response)
    