# AI Redaction

![Workflow diagram of the LLM-powered redaction system.](Workflow_Diagram.png)

This project presents a lightweight, on-premise redaction system that leverages open-source large language models (LLMs) to identify and redact sensitive information without relying on fine-tuning or proprietary APIs. The system is designed as a modular, Dockerized application that exposes a local API, allowing seamless integration into organizational workflows while preserving data locality and privacy. Using prompting alone, the system demonstrates strong redaction performance on a 5,000-example subset of the PII-200k benchmark dataset. Empirical results show that the Gemma 3 12B model significantly outperforms the 4B variant in both redaction accuracy and formatting adherence, with reasonable runtime and high inference stability. While limitations remain in generalization, domain adaptation, and runtime efficiency, the system’s architecture supports horizontal scalability and practical deployment on consumer-grade hardware. All code, prompts, and evaluation configurations are made publicly available to support reproducibility and further development. 

For a deeper look into the design philosophy, system architecture, experimental setup, and broader discussion, the full project write-up is available here:  
📄 [**AI Redaction Project Write-Up (PDF)**](./AI_Redaction_Writeup.pdf)

---

## 📦 Project Structure
```
ai-redaction/
│
├── README.md                      # Main project overview
├── Dockerfile                     # Docker file to build application
├── requirements.txt               # Python dependencies
├── AI_Redaction_Writeup.pdf       # Full project write-up (PDF)
├── Workflow_Diagram.png           # High-level workflow process diagram
│
├── app/                           # FastAPI backend application
│   ├── __init__.py
│   ├── database.py                # Database connection setup
│   ├── inference.py               # Redaction inference logic 
│   ├── main.py                    # FastAPI app entrypoint
│   ├── schemas.py                 # Pydantic schemas for API request/response
│
├── database/                      # Database model definitions (SQLite3)
│   ├── __init__.py
│   ├── models.py                
│
├── experiments/                   # Benchmark experiments and evaluation
│   ├── data/                      # Benchmark datasets
│   │   ├── benchmark_data.csv     
│   │   ├── pii_200k.csv
│   ├── gemma3_4b/                 # Experiment outputs for Gemma 3 4B model
│   │   ├── redacted_errors.csv
│   │   ├── redacted_outputs.csv
│   │   ├── evaluation_results.csv
│   ├── gemma3_12b/                # Experiment outputs for Gemma 3 12B model
│   │   ├── redacted_errors.csv
│   │   ├── redacted_outputs.csv
│   │   ├── evaluation_results.csv
│   ├── scripts/                       # Scripts for experiments
│   │   └── extract_benchmark_data.py  # Extract benchmark data
│   │   ├── run_redaction.py           # Run model inference
│   │   ├── evaluate_redactions.py     # Calculate evaluation metrics
│
├── models/                        # Ollama Modelfiles for local models
│   ├── gemma3_4b/
│   │   ├── Modelfile
│   │   └── README.md
│   ├── gemma3_12b/
│   │   ├── Modelfile
│   │   └── README.md
│
├── scripts/                      
│   ├── send_redact_request.py     # Send request to the /redact endpoint
```

--- 

## 🚀 Quick Start

### 1. Install Ollama and Docker
Make sure [Ollama](https://ollama.com/) and [Docker](https://www.docker.com/) are installed on your computer. 

### 2. Create Ollama models
```bash
ollama create redaction:4b -f ./models/gemma3_4b/Modelfile.txt 
ollama create redaction:12b -f ./models/gemma3_4b/Modelfile.txt 
```
- `ollama list` to verify models were built
- `ollama serve` to verify ollama is running


### 3. Build the Docker image 
```bash
docker build -t ai-redaction -f ./Dockerfile .    
```

### 4. Run the FastAPI Server using the Docker container
```bash
docker run -d -p 8000:8000 ai-redaction
```
The API will be available at `http://localhost:8000/`.

### 5. Test FastAPI Application
- Navigate to `http://localhost:8000/docs`. 
- Click on the `/redact` dropdown
- Press `Try it out`
- Send requests 
- Or run `python scripts/send_redact_request.py` 