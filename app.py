import streamlit as st
from reddit_scraper import get_reddit_user_data
from persona_generator import get_full_persona
from urllib.parse import urlparse
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="Reddit Persona Generator", layout="centered")
st.title(" Reddit User Persona Generator")

# Extract Reddit username from URL
def extract_username(url):
    parts = urlparse(url).path.strip("/").split('/')
    if len(parts) >= 2 and parts[0].lower() == "user":
        return parts[1]
    return None

# Input form
with st.form("user_input_form"):
    reddit_url = st.text_input("Enter Reddit Profile URL", placeholder="https://www.reddit.com/user/username")
    submitted = st.form_submit_button("🔍 Generate Persona")

if submitted:
    username = extract_username(reddit_url)

    if not username:
        st.error("❌ Invalid Reddit profile URL.")
    else:
        st.info(f"🔎 Fetching data for user: u/{username}...")

        posts, comments = get_reddit_user_data(username)

        if not posts and not comments:
            st.error("❌ No posts or comments found.")
        else:
            with st.spinner("🧠 Generating persona using Groq (LLaMA3)... Please wait, it might take a few minutes to process."):
                persona = get_full_persona(posts, comments, username)

            st.success("✅ Persona generated successfully!")
            st.markdown("### 👤 User Persona:")
            st.text(persona)

            # Save to bytes for download
            filename = f"{username}_persona.txt"
            persona_bytes = persona.encode("utf-8")

            st.download_button(
                label="⬇️ Download Persona as .txt",
                data=persona_bytes,
                file_name=filename,
                mime="text/plain"
            )
