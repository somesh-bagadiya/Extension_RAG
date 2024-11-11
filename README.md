# Chrome Extension with Backend for Text Extraction and Query Processing

This project is a Chrome extension integrated with a FastAPI backend for extracting text from web pages and processing user queries using retrieval-augmented generation (RAG). The Chrome extension allows users to extract visible text from a webpage and submit queries, which are then processed by the backend server. The backend utilizes NVIDIA's LLMs for generating responses and ChromaDB for efficient storage and retrieval of embeddings.

## Repository Structure

├── Backend 
    │ └── main.py # FastAPI server to handle text processing and query requests 
├── Extension 
    │ ├── libs # Contains libraries such as marked.js for rendering Markdown in popup 
    │ ├── background.js # Background script for handling messages and backend communication 
    │ ├── content.js # Content script for extracting visible text from the webpage 
    │ ├── manifest.json # Manifest file for Chrome extension configuration 
    │ ├── popup.html # HTML file for the extension's popup interface 
    │ └── popup.js # JavaScript for popup UI interactions and backend requests     
└── requirements.txt # Python dependencies for the backend


## Features

- **Text Extraction**: Extract visible text from any webpage and display it in the Chrome extension popup.
- **Backend Query Processing**: Send extracted text to a FastAPI backend, which processes the text and stores embeddings using ChromaDB.
- **User Query Handling**: Allows users to ask questions in the extension popup, with the backend providing responses using NVIDIA’s large language models.

---

## Prerequisites

- **Python 3.8+** for running the backend server.
- **Node.js** (optional, for development purposes with JavaScript).
- **Google Chrome** (latest version) for loading the extension.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

2. Set Up the Backend
Step 2.1: Create a Virtual Environment
bash
Copy code
python -m venv venv
Step 2.2: Activate the Virtual Environment
Windows:
bash
Copy code
.\venv\Scripts\activate
macOS/Linux:
bash
Copy code
source venv/bin/activate
Step 2.3: Install Dependencies
Install the required Python packages specified in requirements.txt:

bash
Copy code
pip install -r requirements.txt
Step 2.4: Set Up NVIDIA API Key
Obtain an NVIDIA API key (for LLM access).

Create a .env file in the root directory of the backend and add your NVIDIA API key:

bash
Copy code
NVIDIA_API_KEY=your_nvidia_api_key_here
3. Set Up the Chrome Extension
Navigate to Chrome Extensions Page: Open Chrome and go to chrome://extensions/.
Enable Developer Mode: Toggle "Developer mode" on in the top right corner.
Load Unpacked: Click "Load unpacked" and select the Extension folder in this repository.
Running the Project
1. Start the Backend Server
Make sure you are in the root directory where main.py is located, then run:

bash
Copy code
uvicorn Backend.main:app --reload
The FastAPI server should start at http://127.0.0.1:8000.

2. Use the Chrome Extension
Click on the Chrome extension icon in the toolbar to open the popup.
Extract Text: Click "Extract Text" to extract visible text from the current webpage.
Send Query: Type a query and click "Send Query" to get a response from the backend.
Project Structure Details
Backend
main.py: Main entry point for the FastAPI server. Defines endpoints to handle text processing and query requests.
Extension
background.js: Manages background tasks, such as handling messages from popup.js and communicating with the backend.
content.js: Extracts visible text from the current webpage and sends it to popup.js.
manifest.json: Configures the Chrome extension, including permissions and scripts.
popup.html: HTML structure for the Chrome extension popup.
popup.js: JavaScript for managing interactions in the popup, such as sending requests to background.js and handling UI elements.
API Endpoints
The backend provides the following endpoints:

POST /process-text/: Accepts extracted text from the Chrome extension, processes it, and stores embeddings in ChromaDB.
POST /process-query/: Accepts user queries, retrieves relevant embeddings, and generates a response using NVIDIA's language models.
Example Usage
Navigate to any webpage in Chrome.
Click the extension icon, then click "Extract Text" to retrieve visible text.
Enter a question or query in the input box and click "Send Query".
The extension will display a response in the popup.
Troubleshooting
Error: NVIDIA API Key Missing: Ensure that the .env file contains your NVIDIA API key.
Extension Not Loading: Verify that you’ve loaded the Extension folder in Chrome’s chrome://extensions page.
License
This project is licensed under the MIT License. See LICENSE for details.

Acknowledgments
NVIDIA for providing LLM and embedding APIs.
The ChromaDB library for efficient vector storage and retrieval.
