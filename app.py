import streamlit as st
from groq import Groq
import io
import pypdf

GROQ_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "llama3-8b-8192",
    "gemma2-9b-it",
]

st.set_page_config(page_title="AI Chat Assistant", page_icon="🤖", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0f1117; }
    section[data-testid="stSidebar"] { background-color: #1a1d27; border-right: 1px solid #2e3047; }
    section[data-testid="stSidebar"] * { color: #c9d1d9 !important; }
    h1 { color: #ffffff !important; font-size: 1.8rem !important; }
    .stCaption { color: #8b949e !important; }

    [data-testid="stChatMessage"] {
        border-radius: 16px;
        padding: 12px 16px;
        margin: 6px 0;
        max-width: 80%;
    }
    [data-testid="stChatMessage"][data-message-author-role="user"] {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        margin-left: auto;
        border-bottom-right-radius: 4px;
    }
    [data-testid="stChatMessage"][data-message-author-role="assistant"] {
        background-color: #1e2030;
        margin-right: auto;
        border-bottom-left-radius: 4px;
        border: 1px solid #2e3047;
    }
    [data-testid="stChatMessage"] p { color: #f0f0f0 !important; }

    .stChatInput textarea {
        background-color: #1e2030 !important;
        border: 1px solid #2e3047 !important;
        color: #f0f0f0 !important;
        border-radius: 12px !important;
    }

    .stSelectbox > div > div {
        background-color: #1e2030 !important;
        border: 1px solid #2e3047 !important;
        border-radius: 8px !important;
        color: #f0f0f0 !important;
    }
    .stButton > button {
        border-radius: 10px !important;
        background: linear-gradient(135deg, #ef4444, #dc2626) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
    }
    .stButton > button:hover {
        opacity: 0.85 !important;
    }
    div[data-testid="stFileUploader"] {
        background-color: #1e2030;
        border: 1px dashed #2e3047;
        border-radius: 10px;
        padding: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Load API key from secrets or input
api_key = st.secrets.get("GROQ_API_KEY", "")

# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Settings")

    if not api_key:
        api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
        st.caption("Get a free key at console.groq.com")

    model = st.selectbox("🧠 Model", GROQ_MODELS)

    st.markdown("---")
    st.markdown("### 📎 File Upload")
    uploaded_file = st.file_uploader(
        "Attach a file to your message",
        type=["txt", "pdf", "md"],
        label_visibility="collapsed"
    )
    if uploaded_file:
        st.success(f"Attached: {uploaded_file.name}")

    st.markdown("---")
    st.markdown("### 🎙️ Voice Input")
    audio_input = st.audio_input("Record a voice message")

    st.markdown("---")
    st.markdown("### 💬 History")
    if st.session_state.get("messages"):
        for msg in st.session_state["messages"]:
            icon = "🧑" if msg["role"] == "user" else "🤖"
            preview = msg["content"][:50] + ("..." if len(msg["content"]) > 50 else "")
            st.markdown(f"{icon} {preview}")
    else:
        st.info("No messages yet.")

    st.markdown("---")
    if st.button("🔄 Reset Conversation", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        "You are a helpful, accurate, and concise AI assistant. "
        "Answer questions clearly, stay on topic, and do not repeat yourself."
    )
}

# Header
st.markdown("# 🤖 AI Chat Assistant")
st.caption("Powered by Groq — fast, free, and intelligent")
st.markdown("---")

# Display conversation
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Helper: extract text from file
def extract_file_text(file):
    if file.type == "application/pdf":
        reader = pypdf.PdfReader(io.BytesIO(file.read()))
        return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    else:
        return file.read().decode("utf-8", errors="ignore")

# Helper: transcribe voice
def transcribe_audio(audio_bytes, api_key):
    client = Groq(api_key=api_key)
    transcription = client.audio.transcriptions.create(
        file=("voice.wav", audio_bytes, "audio/wav"),
        model="whisper-large-v3",
    )
    return transcription.text

# Handle voice input
voice_text = ""
if audio_input and api_key:
    with st.spinner("Transcribing voice..."):
        try:
            voice_text = transcribe_audio(audio_input.read(), api_key)
            st.info(f"🎙️ Transcribed: {voice_text}")
        except Exception as e:
            st.error(f"Voice transcription failed: {str(e)}")

# Chat input
user_input = st.chat_input("Type your message here...") or voice_text

if user_input:
    if not api_key:
        st.warning("Please enter your Groq API key in the sidebar.")
        st.stop()

    # Append file content if uploaded
    full_message = user_input
    if uploaded_file:
        file_text = extract_file_text(uploaded_file)
        full_message += f"\n\n--- Attached File: {uploaded_file.name} ---\n{file_text[:3000]}"

    st.session_state["messages"].append({"role": "user", "content": full_message})
    with st.chat_message("user"):
        st.markdown(user_input)
        if uploaded_file:
            st.caption(f"📎 {uploaded_file.name} attached")

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                client = Groq(api_key=api_key)
                response = client.chat.completions.create(
                    model=model,
                    messages=[SYSTEM_MESSAGE] + st.session_state["messages"],
                    max_tokens=512,
                    temperature=0.7,
                    stream=True,
                )

                full_response = ""
                placeholder = st.empty()
                for chunk in response:
                    token = chunk.choices[0].delta.content or ""
                    full_response += token
                    placeholder.markdown(full_response + "▌")

                placeholder.markdown(full_response)
                st.session_state["messages"].append(
                    {"role": "assistant", "content": full_response}
                )

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")