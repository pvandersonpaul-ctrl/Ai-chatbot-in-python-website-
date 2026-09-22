
import streamlit as st
from groq import Groq

# Use Secrets, not your real key in code
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(page_title="GIHS AI Chatbot", page_icon="🎓")
st.title("🎓 GIHS AI")

SYSTEM_MSG = "Always format your output using clear line breaks. Emphasize key terms by using ALL CAPS (e.g., IMPORTANT:) instead of markdown asterisks. Use clear plain-text dividers like '===' for headings. Give clean clear structured tables using plain characters."

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_MSG}]
    st.session_state.history = []

for chat in st.session_state.history:
    st.chat_message(chat["role"]).write(chat["content"])

if prompt := st.chat_input("Type your question..."):
    st.session_state.history.append({"role":"user","content":prompt})
    st.session_state.messages.append({"role":"user","content":prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        box = st.empty()
        full = ""
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=st.session_state.messages,
            temperature=1,
            max_completion_tokens=2048,
            top_p=1,
            reasoning_effort="medium",
            stream=True
        )
        for chunk in completion:
            full += chunk.choices[0].delta.content or ""
            box.write(full)

        st.session_state.history.append({"role":"assistant","content":full})
        st.session_state.messages.append({"role":"assistant","content":full})
