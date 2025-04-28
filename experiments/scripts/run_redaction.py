import requests
import pandas as pd
import os
import json


def run_redaction(ollama_model="redaction:4b", save_as_csv=False):
    """
    Run the redaction API on the benchmark data. 
    This function is used to test the redaction API. 
    """

    # Load the benchmark data
    df = pd.read_csv("./experiments/data/benchmark_data.csv")

    # Get only the first 5 rows (as a test)
    df = df.head(5)

    for index, row in df.iterrows():
        try:
            
            # Send the request to the redaction API
            json_response = requests.post(
                "http://127.0.0.1:8000/redact", 
                json={
                    "id": str(row['id']),
                    "input_text": row['source_text'],
                    "model": ollama_model,
                    "add_to_db": False
                }
            )

            # Convert the response to a json object
            json_obj = json_response.json()

            # Create a pandas dataframe from the json object
            redaction_record = pd.DataFrame([{
                "id": json_obj["id"],
                "redacted_text": json_obj["redacted_text"],
                "redacted_cases": json_obj["redacted_cases"],
                "total_duration_seconds": json_obj["total_duration_seconds"],
                "created_at": json_obj["created_at"],
                "model": json_obj["model"]
            }])

            if save_as_csv:
                # Save the json object to a pandas dataframe file
                redaction_record.to_csv(f"./experiments/redaction_records.csv", mode='a', header=not os.path.exists(f"redaction_records.csv"), index=False)   
            
            # Print out the redaction record
            print(f"Succesfully redaction for id: {json_obj['id']}")
            print(redaction_record)

        except Exception as e:
            error_row = pd.DataFrame([{
                "id": str(row['id']),
                "error": str(e)
            }])

            # Print out the error
            print(f"Error for id: {row['id']}")
            print(error_row)

            if save_as_csv:
                error_row.to_csv("errors.csv", mode='a', header=not os.path.exists("errors.csv"), index=False)

            continue


if __name__ == "__main__":

    # Run the redaction API on the benchmark data as a test, assuming FastAPI is running without docker
    run_redaction(ollama_model="redaction:4b", save_as_csv=False)
    