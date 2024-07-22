import streamlit as st
from openai import OpenAI

with st.sidebar:
    system_opition = st.text_input("ユーザー名を入力してください")
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

client = OpenAI(api_key=openai_api_key)

avatar_url = "str/images/karin-2.png"
avatar_url_me = "str/images/me.png"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message.get("avatar")):
        st.markdown(message["content"])


if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": avatar_url_me})
    with st.chat_message("aketami", avatar=avatar_url_me):
        st.markdown(prompt)

    with st.chat_message("karin", avatar=avatar_url):
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_opition}
            ] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            temperature=1,
            max_tokens=256,
            stream=True
        )
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response, "avatar": avatar_url})
    