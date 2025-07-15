
import os
import time
import requests
import re
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-70b-8192"

# Configurable max number of total chunks (split evenly between posts and comments)
MAX_TOTAL_CHUNKS = int(os.getenv("MAX_TOTAL_CHUNKS", 20))
HALF_CHUNKS = MAX_TOTAL_CHUNKS // 2


def chunk_data(data_list, chunk_size=1):
    for i in range(0, len(data_list), chunk_size):
        yield data_list[i:i + chunk_size]


def generate_prompt_chunk(posts, comments, username):
    intro = f"""
You are a behavioral analyst. ALL of the following Reddit posts and comments were written by the same user: u/{username}.

Your task is to analyze their language, content, tone, and behavior to create a professional-level user persona report.

---
**Username:** {username}

# 🎂 Estimated Age Range:
# 💼 Likely Occupation / Background:
# 🎯 Motivations / Values:
# 🧠 Thinking Style / Communication Style:
# 📱 Online Behavior Patterns:
# 💬 Personality Traits (with evidence or citations):
# 🎮 Interests / Hobbies / Expertise Areas:
# 😤 Frustrations / Pet Peeves:
# 🧠 Summary Insight:

Please  don't cite post/comment 
---
"""
    content = ""
    for i, post in enumerate(posts):
        if post["text"].strip():
            content += f"\nPOST {i+1}:\nTitle: {post['title']}\nText: {post['text']}\nURL: {post['url']}\n"
    for i, comment in enumerate(comments):
        if comment["text"].strip():
            content += f"\nCOMMENT {i+1}:\nText: {comment['text']}\nURL: {comment['url']}\n"

    full_prompt = intro.strip() + "\n\n" + content.strip()
    return full_prompt[:18000]  # Safe cap to avoid 413 error


def get_persona_from_groq_chunk(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a professional behavioral analyst."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1024
    }

    response = requests.post(GROQ_ENDPOINT, headers=headers, json=data)

    if response.status_code != 200:
        raise Exception(f"Groq returned {response.status_code}: {response.text}")

    return response.json()["choices"][0]["message"]["content"]


def retry_groq(prompt, retries=3):
    for attempt in range(retries):
        try:
            return get_persona_from_groq_chunk(prompt)
        except Exception as e:
            error_msg = str(e)

            if "413" in error_msg:
                print("🚫 Request too large. Skipping this chunk.")
                return f"Chunk failed due to prompt too large: {e}"

            match = re.search(r'try again in ([\d.]+)s', error_msg)
            wait_time = float(match.group(1)) if match else 15

            if "429" in error_msg and attempt < retries - 1:
                print(f"⏳ Rate limit hit. Waiting {wait_time:.1f}s...")
                time.sleep(wait_time + 1)
            else:
                print(f"❌ Final failure: {e}")
                return f"Chunk failed: {e}"


def get_full_persona(posts, comments, username):
    print("📦 Splitting content into 10 chunks (5 posts + 5 comments)...")

    # Filter and trim posts/comments to limit total Groq requests
    posts = [p for p in posts if p.get("text") and p["text"].strip()][:HALF_CHUNKS]
    comments = [c for c in comments if c.get("text") and c["text"].strip()][:HALF_CHUNKS]

    post_chunks = list(chunk_data(posts, chunk_size=1))
    comment_chunks = list(chunk_data(comments, chunk_size=1))

    max_chunks = max(len(post_chunks), len(comment_chunks))
    partial_personas = []

    for i in range(max_chunks):
        print(f"🧠 Processing chunk {i+1}/{max_chunks}...")

        post_chunk = post_chunks[i] if i < len(post_chunks) else []
        comment_chunk = comment_chunks[i] if i < len(comment_chunks) else []

        prompt = generate_prompt_chunk(post_chunk, comment_chunk, username)
        summary = retry_groq(prompt)
        partial_personas.append(summary)

    print("🔁 Consolidating all partial insights into final persona...")

    # Join partial summaries and truncate to safe size
    partial_text = "\n\n".join(partial_personas)
    partial_text = partial_text[:16000]

    final_prompt = f"""
You are a professional behavioral analyst.

The following are partial persona summaries derived from Reddit activity by u/{username}.

Your job is to merge and distill all this information into ONE final, polished, non-redundant user persona.

The final output must follow this format:

**Username:** {username}

# 🎂 Estimated Age Range:
# 💼 Likely Occupation / Background:
# 🎯 Motivations / Values:
# 🧠 Thinking Style / Communication Style:
# 📱 Online Behavior Patterns:
# 💬 Personality Traits (with citations if possible):
# 🎮 Interests / Hobbies / Expertise Areas:
# 😤 Frustrations / Pet Peeves:
# 🧠 Summary Insight:

Be clear, professional, and focused only on u/{username}.

---

Partial insights:
""" + partial_text

    final_output = retry_groq(final_prompt)
    return final_output
