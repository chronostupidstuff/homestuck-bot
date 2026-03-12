import random
import requests
import tweepy
import os

# Twitter authentication
client = tweepy.Client(
    consumer_key=os.getenv("API_KEY"),
    consumer_secret=os.getenv("API_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
)

# Homestuck unofficial API
API_URL = "https://api.homestuck.net/v1"

def get_random_page():
    story = requests.get(f"{API_URL}/story").json()

    # Filter Homestuck pages
    pages = [p for p in story if p["story"] == "homestuck"]

    page = random.choice(pages)

    page_id = page["pageId"]
    title = page["title"]

    media = page.get("media", [])
    img_url = None

    for m in media:
        if m.endswith(".png") or m.endswith(".gif") or m.endswith(".jpg"):
            img_url = m
            break

    return page_id, title, img_url


def post_tweet():
    page_id, title, img_url = get_random_page()

    if not img_url:
        return

    img_data = requests.get(img_url).content

    with open("panel.png", "wb") as f:
        f.write(img_data)

    auth = tweepy.OAuth1UserHandler(
        os.getenv("API_KEY"),
        os.getenv("API_SECRET"),
        os.getenv("ACCESS_TOKEN"),
        os.getenv("ACCESS_TOKEN_SECRET")
    )

    api = tweepy.API(auth)

    media = api.media_upload("panel.png")

    tweet_text = f"Page {page_id}: {title}"

    client.create_tweet(text=tweet_text, media_ids=[media.media_id])


if __name__ == "__main__":
    post_tweet()
