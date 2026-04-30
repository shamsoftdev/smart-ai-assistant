import streamlit as st
import requests
from pydantic import BaseModel

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Smart AI Assistant", layout="wide")

# ---------------------------
# SESSION STATE
# ---------------------------
if "token" not in st.session_state:
    st.session_state.token = None

# ---------------------------
# LOGIN
# ---------------------------
st.title("🤖 Smart AI Assistant")

if not st.session_state.token:
    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        res = requests.post(
            f"{BASE_URL}/auth/login",
            json={"username": username, "password": password}
        )

        if res.status_code == 200:
            st.session_state.token = res.json()["access_token"]
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

# ---------------------------
# MAIN APP
# ---------------------------
else:
    st.sidebar.success("Logged in")
    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.rerun()

    menu = st.sidebar.radio("Select Feature", [
        "Chatbot",
        "Resume Analyzer",
        "Email Generator"
    ])

    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

    # ---------------------------
    # CHATBOT
    # ---------------------------
    if menu == "Chatbot":
        st.subheader("💬 Chat with AI")

        
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        user_input = st.text_input("Enter your message")

        if st.button("Send"):
                try:
                 res = requests.post(
                      f"{BASE_URL}/ai/chat",
                    headers=headers,
                     json={"message": user_input}
                 )
                 data = res.json()
                 st.write("💬", data["response"])
                # st.write("STATUS:", res.status_code)
                # st.write("RESPONSE:", res.text)
                except Exception as e:
                   st.error(f"Request failed: {e}")         
 
    # Display chat
        for role, msg in st.session_state.chat_history:
              st.write(f"**{role}:** {msg}")

    # ---------------------------
    # RESUME ANALYZER
    # ---------------------------
    elif menu == "Resume Analyzer":
        st.subheader("📄 Resume Analyzer")

        resume = st.text_area("Paste Resume")
        job_desc = st.text_area("Paste Job Description")

        if st.button("Analyze"):
            res = requests.post(
                f"{BASE_URL}/ai/analyze",
                headers=headers,
                json={
                    "resume_text": resume,
                    "job_description": job_desc
                }
            )

            if res.status_code == 200:
                st.json(res.json())
            else:
                st.error(res.text)

    # ---------------------------
    # EMAIL GENERATOR
    # ---------------------------
    elif menu == "Email Generator":
        st.subheader("✉️ Generate Email")

        purpose = st.text_input("Purpose")
        tone = st.selectbox("Tone", ["Professional", "Casual"])
        context = st.text_area("Context")

        if st.button("Generate"):
            res = requests.post(
                f"{BASE_URL}/ai/generate-email",
                headers=headers,
                json={
                    "purpose": purpose,
                    "tone": tone,
                    "context": context
                }
            )

            if res.status_code == 200:
                data = res.json()
                st.subheader("Subject")
                st.write(data["subject"])

                st.subheader("Email Body")
                st.write(data["email_body"])
            else:
                st.error(res.text)