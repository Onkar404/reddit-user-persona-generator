import os
from urllib.parse import urlparse
from reddit_scraper import get_reddit_user_data
from persona_generator import get_persona_from_groq
from dotenv import load_dotenv

load_dotenv()

def extract_username(url):
    """
    Extracts the Reddit username from a profile URL like:
    https://www.reddit.com/user/kojied → kojied
    """
    parts = urlparse(url).path.strip("/").split('/')
    if len(parts) >= 2 and parts[0].lower() == "user":
        return parts[1]
    return None

def save_persona_to_file(username, persona_text):
    filename = f"{username}_persona.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(persona_text)
    print(f"\n✅ Persona saved to: {filename}")

if __name__ == "__main__":
    url = input("🔗 Enter Reddit profile URL (e.g. https://www.reddit.com/user/kojied): ").strip()
    username = extract_username(url)

    if not username:
        print("❌ Invalid Reddit URL format.")
        exit()

    print(f"\n🔍 Scraping Reddit data for user: u/{username} ...")
    posts, comments = get_reddit_user_data(username)

    if not posts and not comments:
        print("❌ No Reddit posts or comments found for this user.")
        exit()

    print("\n🧠 Generating persona using Groq (LLaMA3)... Please wait.")
    persona = get_persona_from_groq(posts + comments, username)

    print("\n📄 Persona:\n")
    print(persona)

    save_persona_to_file(username, persona)
