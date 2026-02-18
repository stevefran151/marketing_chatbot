# Marketing Chatbot

A specialized AI-powered marketing assistant chatbot that helps users with marketing, branding, and business growth questions.

## 🚀 Features

- **Specialized Knowledge**: Strictly focused on marketing, branding, advertising, and growth strategies.
- **RAG Architecture**: Uses **LangChain** for Retrieval-Augmented Generation (RAG) to fetch relevant context from the vector store.
- **Context Awareness**: Leverages **LangChain's History** capabilities to remember conversation context for seamless follow-up questions.
- **Text-to-Speech (TTS)**: Built-in TTS toggle to read responses aloud.
- **Modern UI**: Dark-themed, responsive, and animated chat interface.
- **Voice Agent (Deprecated)**: The project previously supported a voice-to-voice agent but is now focused on text/chat interactions.

## 📂 Project Architecture

The project is structured into clear Frontend and Backend components:

```
marketing_chatbot/
├── backend/                # Python/Flask Backend
│   ├── app.py              # Main application entry point
│   ├── src/                # Source code for logic & prompts
│   │   ├── helper.py       # Embeddings & utility functions
│   │   └── prompt.py       # System prompts & instructions
│   ├── data/               # Data directory for RAG content
│   ├── store_index.py      # Script to process & index data
│   ├── requirements.txt    # Python dependencies
│   └── .env                # Environment variables
│
├── frontend/               # Web Interface
│   ├── templates/          # HTML templates (chat.html)
│   └── static/             # Static assets (CSS/JS/Images)
│
└── README.md               # Project Documentation
```

## 🛠️ Technology Stack

- **Backend**: Python, Flask, LangChain
- **AI/LLM**: Groq (Llama 3.1), Google Gemini (Embeddings), Pinecone (Vector Database)
- **Frontend**: HTML5, CSS3 (Bootstrap + Custom Animations), JavaScript (jQuery)
- **Tools**: Dotenv for configuration

## ⚡ How to Run

1.  **Prerequisites**:
    -   Python 3.8+ installed.
    -   API Keys for **Pinecone**, **Groq**, and **Google Generative AI**.

2.  **Environment Setup**:
    -   Navigate to the `backend` folder.
    -   Ensure your `.env` file is present containing:
        ```
        PINECONE_API_KEY=your_key
        GROQ_API_KEY=your_key
        GOOGLE_API_KEY=your_key
        ```

3.  **Install Dependencies**:
    ```bash
    cd backend
    pip install -r requirements.txt
    ```

4.  **Run the Application**:
    ```bash
    python app.py
    ```
    The server will start at `http://localhost:8080`.

## 🧠 Flow Overview

1.  **User Input**: User sends a message via the web interface.
2.  **Backend Processing**:
    -   `app.py` receives the message.
    -   **Contextualization**: If it's a follow-up question, it's rephrased to be standalone.
    -   **Retrieval**: The system searches the Pinecone vector store for relevant marketing documents.
    -   **Generation**: The LLM generates a concise, marketing-focused answer using the retrieved context.
3.  **Response**: The answer is sent back to the frontend.
4.  **Display & TTS**: The frontend displays the message with an animation and optionally reads it aloud using the Web Speech API.

