
# 🧠 Reddit User Persona Generator

This project generates a professional behavioral **user persona** based on a Reddit user's **posts** and **comments**.  
It uses **PRAW** for scraping Reddit and **Groq’s LLaMA3 model** to analyze user behavior, tone, values, and interests.

> Ideal for: LLM profiling, behavioral research, NLP-powered tools, or just for fun insights into Reddit users!

---

## 🚀 Features

- 🔍 Input any Reddit profile URL (e.g. `https://www.reddit.com/user/some_user`)
- 📄 Scrapes that user's latest Reddit posts & comments (up to 30 each)
- 🧠 Builds a detailed user persona using Groq LLaMA3 (`llama3-70b-8192`)
- 📉 Rate-limit safe (max 10 requests per user)
- 🖼️ Optional Streamlit GUI included
- 💬 Persona is saved in `.txt` format and can be downloaded

---

## 🧰 Tech Stack

- **Python 3.9+**
- [PRAW](https://praw.readthedocs.io/) – Reddit scraping
- [Groq API](https://console.groq.com/) – LLaMA3 for persona generation
- [Streamlit](https://streamlit.io/) – For web interface
- `.env`-based config with [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/Onkar404/reddit-user-persona-generator.git
cd reddit-user-persona-generator
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate        # on Linux/macOS
venv\Scripts\activate           # on Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔐 .env Configuration

Create a `.env` file in the project root:

```env
REDDIT_CLIENT_ID=your_reddit_app_client_id
REDDIT_CLIENT_SECRET=your_reddit_app_client_secret
REDDIT_USER_AGENT=reddit_persona_app

GROQ_API_KEY=your_groq_api_key
MAX_TOTAL_CHUNKS=10  # optional: number of chunks to send to Groq
```

### 🔑 How to get these:

- **Reddit keys**: [Create a Reddit app](https://www.reddit.com/prefs/apps) under "script" type.
- **Groq key**: [Sign up at Groq](https://console.groq.com/) and generate an API key.

---

## 🧪 Run the Project (Terminal version)

To generate a persona from a Reddit profile in the terminal:

```bash
python main.py
```

You’ll be prompted to enter a Reddit profile URL.  
The generated persona will be printed and saved as a `.txt` file.

---

## 🌐 Optional: Run the Streamlit UI

If you prefer a web interface, run:

```bash
streamlit run app.py
```

You'll get a web form to enter the Reddit URL and download the result.

---

## 📄 Sample Output

The persona looks like this:

```
**Username:** Opposite_Wait

# 🎂 Estimated Age Range: Late 20s to early 30s
# 💼 Likely Occupation / Background: Software development or tech
# 🎯 Motivations / Values: Efficiency, control, problem-solving
# 🧠 Thinking Style / Communication Style: Logical, sarcastic, clear
# 📱 Online Behavior Patterns: Tech-focused subreddits, witty comments
...
```

Full sample in `Opposite_Wait_persona.txt`

---

## 🧠 How It Works

1. **Reddit scraper** (PRAW) gathers user's last 30 posts and comments.
2. The data is split into small chunks (to stay under Groq’s token limits).
3. Each chunk is analyzed via LLaMA3 (Groq API) to get partial summaries.
4. The partials are merged into a single final professional persona.

---

## 🧱 File Structure

```
├── app.py                  # Streamlit interface
├── main.py                 # Terminal runner
├── reddit_scraper.py       # Reddit data fetcher
├── persona_generator.py    # Groq LLM analysis logic
├── requirements.txt
├── .env.example            # Sample environment config
├── README.md
```

---

## 🧠 Author

Built by Onkar Nigdikar 


---

## 📄 License

This project is licensed under the MIT License.
