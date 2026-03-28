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
    [data-testid="stChatMessage"][data-message-author-role="user"] {
        background: linear-gradient(135deg, #4f8ef7, #2563eb);
        border-radius: 16px;
        margin-left: 15%;
        border-bottom-right-radius: 4px;
        padding: 12px 16px;
    }
    [data-testid="stChatMessage"][data-message-author-role="user"] p {
        color: #ffffff !important;
    }
    [data-testid="stChatMessage"][data-message-author-role="assistant"] {
        background-color: #ffffff;
        border-radius: 16px;
        margin-right: 15%;
        border-bottom-left-radius: 4px;
        border: 1px solid #c5cde0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        padding: 12px 16px;
    }
    .stButton > button {
        border-radius: 10px !important;
        background: linear-gradient(135deg, #ef4444, #dc2626) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
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
    st.markdown("### 📎 Attach File")
    uploaded_file = st.file_uploader(
        "Upload file",
        type=["txt", "pdf", "md"],
        label_visibility="collapsed"
    )
    if uploaded_file:
        st.success(f"✅ {uploaded_file.name}")

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

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    if not api_key:
        st.warning("Please enter your Groq API key in the sidebar.")
        st.stop()

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