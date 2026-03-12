import os
import random
import requests
import tweepy

# -----------------------
# Twitter Authentication
# -----------------------
auth = tweepy.OAuth1UserHandler(
    os.getenv("API_KEY"),
    os.getenv("API_SECRET"),
    os.getenv("ACCESS_TOKEN"),
    os.getenv("ACCESS_TOKEN_SECRET")
)
api = tweepy.API(auth)

# Test auth
try:
    api.verify_credentials()
    print("Authentication OK")
except Exception as e:
    print("Error during authentication:", e)

# -----------------------
# Homestuck Panel Info
# -----------------------
BASE_URL = "https://storage.homestuck.com/story/homestuck/media/images/panels/"

# Example acts with page counts (update to actual counts)
ACTS = {
    "act-1": 31,
    "act-2": 25,
    "act-3": 50,
}

def get_random_panel():
    act = random.choice(list(ACTS.keys()))
    page_num = random.randint(1, ACTS[act])
    page_str = str(page_num).zfill(5)

    # Check for valid image extension
    for ext in [".gif", ".png", ".jpg"]:
        url = f"{BASE_URL}{act}/{page_str}{ext}"
        response = requests.head(url)
        if response.status_code == 200:
            return act, page_num, url
    return None, None, None

# -----------------------
# Post to Twitter/X
# -----------------------
def post_panel():
    act, page_num, url = get_random_panel()
    if not url:
        print("No valid panel found.")
        return

    # Download image
    img_data = requests.get(url).content
    with open("panel.png", "wb") as f:
        f.write(img_data)

    # Upload and tweet
    media = api.media_upload("panel.png")
    tweet_text = f"Page {page_num}: {act.replace('-', ' ').title()}"
    api.update_status(status=tweet_text, media_ids=[media.media_id])
    print(f"Posted: {tweet_text}")

if __name__ == "__main__":
    post_panel()
