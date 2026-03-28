# 🤖 AI Chat Assistant
A fully deployed AI chat web app built with Python and Streamlit, powered by Groq's ultra-fast LLM API.
🔗 **Live Demo:** https://aichatbot-llm.streamlit.app/
💻 **GitHub:** https://github.com/AlishaFatima16/ollama-chat-deployed
---
## What It Does
- 💬 Chat with multiple AI models in real time with streaming responses
- 📄 Upload PDF, TXT, or Markdown files and ask questions about them
- 🧠 Remembers the full conversation within your session
- 🎯 Uses a system prompt to keep answers accurate and on topic
- ⚡ Responses in under 1 second powered by Groq
- 🔄 Reset the conversation anytime with one click
---
## Tech Stack
- **Python** — core language
- **Streamlit** — web interface
- **Groq API** — cloud LLM inference
- **Ollama** — local LLM support (offline version)
- **pypdf** — PDF text extraction
---
## Available Models
- `llama-3.3-70b-versatile`
- `llama-3.1-8b-instant`
- `llama3-8b-8192`
- `gemma2-9b-it`
---
## Run Locally
**1. Clone the repo**
```bash
git clone https://github.com/AlishaFatima16/ollama-chat-deployed.git
cd ollama-chat-deployed
2. Install dependencies

pip install -r requirements.txt
3. Add your API key

Only needed if running locally. The live demo works without any setup.

Create .streamlit/secrets.toml:

GROQ_API_KEY = "gsk_your_key_here"
Get a free key at console.groq.com

4. Run

streamlit run app.py
File Structure
ollama-chat-deployed/
├── app.py                  # Main application
├── requirements.txt        # Dependencies
└── .streamlit/
    ├── config.toml         # Theme and server config
    └── secrets.toml        # API key (never committed to GitHub)
Deploy Your Own
Fork this repo
Go to streamlit.io/cloud and sign in with GitHub
Select your forked repo and set main file to app.py
Add GROQ_API_KEY under Advanced Settings → Secrets
Click Deploy
License
MIT — free to use with credit.

Built by Alisha Fatima