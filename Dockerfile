# FROM python:3.9-slim

# # WORKDIR /app

# # COPY . /app

# RUN apt-get update
# RUN apt-get -y upgrade
# # RUN apt-get -y install python3
# # RUN apt-get -y install python3-pip


# RUN build-essential \
# curl \
# software-properties-common \
# git \
# && rm -rf /var/lib/apt/lists/*

# RUN git clone https://github.com/codemaivanngu/NotebookRAG.git .

# RUN pip3 install -r requirements.txt
# EXPOSE 8501
# HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]

# # RUN apt -y install python3.12-venv
# # RUN python3 -m venv .venv
# # RUN source .venv/bin/activate
# # RUN pip install -r requirements.txt
# #  && pip install -r requirements.txt
# #  && curl -fsSL https://ollama.com/install.sh | sh && ollama run llama3

# # CMD [ "streamlit","run", "main.py"]
# # apt-get install 
# # -y locales && rm -rf /var/lib/apt/lists/* \
# # 	&& localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/codemaivanngu/NotebookRAG.git .

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
