FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://ollama.com/install.sh | sh

COPY . /app
RUN pip3 install -r requirements.txt

# Start ollama service
RUN nohup ollama start & \
    sleep 10 && \
    ollama pull llama3
# RUN ollama serve

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["ollama", 'serve','&&',"streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
