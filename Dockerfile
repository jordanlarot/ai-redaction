FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current project files into the container
COPY ./app /app/app
COPY ./requirements.txt /app/requirements.txt
COPY ./database/__init__.py /app/database/__init__.py
COPY ./database/models.py /app/database/models.py

# Install the dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose the port that FastAPI will run on
EXPOSE 8000

# Set the base URL for the ollama endpoint to run within the docker container
ENV OLLAMA_CHAT_URL=http://host.docker.internal:11434/api/chat

# Command to run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]