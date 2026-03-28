# 🤖 AI Chat Assistant

A fully deployed AI chat web application built with Python and Streamlit, powered by Groq's lightning-fast LLM API. Supports real-time streaming conversations, PDF/file uploads, and multiple AI models.

🔗 **Live App:** https://aichatbot-llm.streamlit.app/

---

## Features

- 💬 Real-time streaming chat with multiple AI models
- 📄 Upload PDFs, TXT, and Markdown files and ask questions from them
- 🧠 Persistent conversation history within the session
- 🎯 System prompt to keep responses accurate and on-topic
- 🔄 One-click conversation reset
- ⚡ Under 1 second responses via Groq inference engine
- 🔐 Secure API key handling via Streamlit secrets

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Streamlit | Web interface |
| Groq API | Cloud LLM inference |
| Ollama | Local LLM support |
| pypdf | PDF text extraction |

---

## Models Supported

- `llama-3.3-70b-versatile`
- `llama-3.1-8b-instant`
- `llama3-8b-8192`
- `gemma2-9b-it`

---

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/AlishaFatima16/ollama-chat-deployed.git
cd ollama-chat-deployed