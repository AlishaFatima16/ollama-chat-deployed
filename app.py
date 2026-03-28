import streamlit as st
from groq import Groq

GROQ_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "llama3-8b-8192",
    "gemma2-9b-it",
]

st.set_page_config(page_title="AI Chat Assistant", page_icon="🤖", layout="centered")
st.title("🤖 AI Chat Assistant")
st.caption("Powered by Groq LLM")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")

    api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
    st.caption("Get a free key at console.groq.com")

    model = st.selectbox("Choose Model", GROQ_MODELS)

    st.markdown("---")
    st.subheader("💬 Conversation History")

    if st.session_state.get("messages"):
        for msg in st.session_state["messages"]:
            role_icon = "🧑" if msg["role"] == "user" else "🤖"
            preview = msg["content"][:60] + ("..." if len(msg["content"]) > 60 else "")
            st.markdown(f"{role_icon} **{msg['role'].capitalize()}:** {preview}")
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

# Display conversation
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    if not api_key:
        st.warning("Please enter your Groq API key in the sidebar to start chatting.")
        st.stop()

    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

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