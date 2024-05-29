Sure! Below is an updated README file for your GitHub project "NotebookRAG" with instructions for using Docker.

---

# NotebookRAG

## Introduction
Welcome to NotebookRAG! This application leverages a local Language Learning Model (LLM), Llama3, through Ollama to provide Retrieval-Augmented Generation (RAG) and chat functionalities based on PDFs and website content, all without sending any data to an online server. NotebookRAG is designed to maintain user privacy and ensure data security while offering robust and interactive text analysis capabilities.

## Technical Overview
NotebookRAG integrates several key components to deliver its functionalities:

1. **Local LLM (Llama3):** Utilizes Llama3, a powerful language model, for natural language understanding and generation.
2. **Ollama:** Acts as the interface for interacting with the Llama3 model locally.
3. **Offline Encoder:** Processes and encodes data from PDFs and websites, ensuring that all content handling is performed offline.
4. **RAG (Retrieval-Augmented Generation):** Enhances the generative capabilities of the LLM by incorporating retrieved documents and snippets from the provided content sources.

### Key Features:
- **Local Processing:** All operations are performed locally, ensuring data privacy and security.
- **PDF and Web Content Integration:** Easily incorporate and analyze text from PDFs and websites.
- **Interactive Chat:** Engage in meaningful conversations with the model based on your documents and data.

## How to Install

### Prerequisites
- Docker

### Installation Steps

1. **Install Docker:**
   - Follow the instructions on the [Docker website](https://docs.docker.com/get-docker/) to install Docker on your system.

2. **Download the NotebookRAG Docker image:**
   ```bash
   docker pull codemaivanngu/note_rag:latest
   ```

3. **Create and run a Docker container:**
   ```bash
   docker run -d -p 8501:8501 --name notebookrag_container codemaivanngu/note_rag:latest
   ```

   This command will create and run a Docker container named `notebookrag_container` from the downloaded image and map port 8080 of the container to port 8080 of your host machine.

## Usage

### Accessing the Application
0. **Create and run a Docker container:**
   ```bash
   docker run -d -p 8501:8501 --name notebookrag_container codemaivanngu/note_rag:latest
   ```
1. **Open your web browser and navigate to:**
   ```
   http://localhost:8501
   ```

2. **Upload PDF or provide website URLs:**
   - Use the provided interface to upload PDFs or input website URLs for analysis.

3. **Interact with the model:**
   - Use the chat functionality to ask questions and interact with the model based on the uploaded content.


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
- Special thanks to the developers of Llama3 and Ollama for their incredible work.
- Thanks to the open-source community for the invaluable tools and resources.
