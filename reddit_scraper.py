import praw
import os
from dotenv import load_dotenv

load_dotenv()

def get_reddit_user_data(username, limit=30):
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
    )

    user = reddit.redditor(username)
    posts = []
    comments = []

    try:
        for post in user.submissions.new(limit=limit):
            posts.append({
                "title": post.title,
                "text": post.selftext,
                "url": f"https://www.reddit.com{post.permalink}"
            })

        for comment in user.comments.new(limit=limit):
            comments.append({
                "text": comment.body,
                "url": f"https://www.reddit.com{comment.permalink}"
            })

    except Exception as e:
        print(f"Error scraping: {e}")

    return posts, comments
