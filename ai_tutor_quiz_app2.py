import os
import time
import streamlit as st
from openai import OpenAI

# --- Streamlit Page Setup ---
st.set_page_config(page_title="AI Tutor & Quiz Generator", page_icon="📘", layout="centered")

# --- API Key Setup ---
API_KEY = os.getenv("OPENAI_API_KEY") or st.sidebar.text_input("🔑 Enter OpenAI API Key", type="password")

# ✅ Set timeout (60s instead of default 10s)
client = OpenAI(api_key=API_KEY, timeout=60.0)

# --- Custom CSS (WhatsApp Business-style with blue chat input) ---
st.markdown("""
<style>
body {
    background-color: #0b141a;
    font-family: 'Segoe UI', sans-serif;
}
.chat-container {
    border-radius: 12px;
    padding: 15px;
    background-color: #111b21;
    max-height: 550px;
    overflow-y: auto;
    margin-bottom: 15px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.4);
}
.user-bubble {
    background-color: #056162;
    color: white;
    padding: 10px 14px;
    border-radius: 18px 18px 0px 18px;
    margin: 8px;
    text-align: right;
    display: inline-block;
    max-width: 75%;
    float: right;
    clear: both;
}
.bot-bubble {
    background-color: #202c33;
    color: #e9edef;
    padding: 10px 14px;
    border-radius: 18px 18px 18px 0px;
    margin: 8px;
    text-align: left;
    display: inline-block;
    max-width: 75%;
    float: left;
    clear: both;
}
.system-bubble {
    background-color: #36454F;
    color: #e9edef;
    padding: 6px 10px;
    border-radius: 10px;
    margin: 10px auto;
    display: table;
    font-size: 12px;
}
.chat-input {
    display: flex;
    align-items: center;
    border: 2px solid #007bff;   /* Blue border */
    border-radius: 8px;
    padding: 2px 8px;
    background-color: #f0f2f6;   
    height: 42px;                /* ✅ Same size as topic input */
}

.chat-input input {
    border: none;
    outline: none;
    flex: 1;
    font-size: 16px;
    background: transparent;
    color: black;
    padding: 6px;
}

.chat-input button {
    background: #007bff;
    border: none;
    cursor: pointer;
    font-size: 16px;
    color: white;
    width: 34px;
    height: 34px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-left: 6px;
}

/* Input box styling inside */
.chat-input input {
    border: none;
    outline: none;
    flex: 1;
    font-size: 16px;
    background: transparent;
    color: black;
}

/* Send button aligned same height */
.chat-input button {
    background: white;  /* Blue background */
    border: none;
    cursor: pointer;
    font-size: 18px;
    color: black;
    padding: 8px 14px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}
/* Topic input box blue border */
div[data-baseweb="input"] > div {
    border: 2px solid #007bff !important;  /* Blue */
    border-radius: 8px;
}

.chat-input button:hover {
    color: #63b3ff; /* lighter blue on hover */
}
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# --- App Title ---
st.markdown("<h2 style='color:#25d366;'>📘 AI Tutor & Quiz Generator</h2>", unsafe_allow_html=True)

# --- Topic Input ---
topic = st.text_input("Enter a topic:", key="topic_input")

# --- Explanation & Quiz Buttons ---
col1, col2 = st.columns(2)
with col1:
    if st.button("📖 Explanation") and topic:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a tutor who explains concepts clearly."},
                    {"role": "user", "content": f"Explain {topic} in simple terms."}
                ]
            )
            explanation = response.choices[0].message.content
            st.session_state["messages"].append(("🤖", explanation))
        except Exception as e:
            st.session_state["messages"].append(("⚠️", f"Error: {e}"))

with col2:
    if st.button("❓ Quiz") and topic:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a tutor who generates quizzes."},
                    {"role": "user", "content": f"Create a 3-question quiz on {topic} with answers."}
                ]
            )
            quiz = response.choices[0].message.content
            st.session_state["messages"].append(("🤖", quiz))
        except Exception as e:
            st.session_state["messages"].append(("⚠️", f"Error: {e}"))

# --- Conversation Display ---
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for sender, msg in st.session_state["messages"]:
    if sender == "👤":
        st.markdown(f'<div class="user-bubble">{msg}</div>', unsafe_allow_html=True)
    elif sender == "🤖":
        st.markdown(f'<div class="bot-bubble">{msg}</div>', unsafe_allow_html=True)
    elif sender == "⚠️":
        st.markdown(f'<div class="system-bubble">{msg}</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
# --- Chat Input Box with Send Button ---
with st.form("chat_form", clear_on_submit=True):
    st.markdown(
        """
        <style>
        .chat-box {
            display: flex;
            align-items: center;
            border: 2px solid #007bff;
            border-radius: 8px;
            background-color: #f0f2f6; /* ✅ same color for box + button */
            padding: 2px 6px;
        }
        .chat-box div[data-baseweb="input"] {
            flex: 1;
            border: none !important;
            background: transparent !important;
        }
        .chat-box button {
            background-color: #f0f2f6 !important; /* ✅ same as box */
            border: none;
            color: black;
            font-size: 16px;
            cursor: pointer;
        }
        .chat-box button:hover {
            color: #007bff;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Layout: input + button inside one styled container
    col1, col2 = st.columns([9, 1])
    with col1:
        user_msg = st.text_input(
            "Type your message...",
            key="chat_message",
            label_visibility="collapsed"
        )
    with col2:
        submitted = st.form_submit_button("➤")  # inside same box
if submitted and user_msg.strip():
    st.session_state["messages"].append(("👤", user_msg))

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a friendly tutor."},
                {"role": "user", "content": user_msg},
            ]
        )
        reply = response.choices[0].message.content
        st.session_state["messages"].append(("🤖", reply))

    except Exception as e:
        st.session_state["messages"].append(("⚠️", f"Error: {e}"))

