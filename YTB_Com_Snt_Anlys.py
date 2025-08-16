import os
import csv
import pandas as pd
from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import re

# Replace with your own API key
API_KEY = 'YOUR_NEW_API_KEY'

# Initialize the YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Define model storage path
MODEL_DIR = "./Models/tabularisai"

# Check if the model directory exists, if not, download the model
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR, exist_ok=True)
    model = AutoModelForSequenceClassification.from_pretrained(
        "tabularisai/multilingual-sentiment-analysis")
    tokenizer = AutoTokenizer.from_pretrained("tabularisai/multilingual-sentiment-analysis")

    model.save_pretrained(MODEL_DIR)
    tokenizer.save_pretrained(MODEL_DIR)

# Load the sentiment analysis pipeline from local directory
sentiment_pipeline = pipeline(
    "text-classification",
    model=MODEL_DIR,
    tokenizer=MODEL_DIR
)


def get_video_id_from_url(url):
    """Extracts the video ID from a YouTube URL."""
    try:
        parsed_url = urlparse(url)
        if parsed_url.netloc in ['www.youtube.com', 'youtube.com']:
            query = parse_qs(parsed_url.query)
            video_id = query.get('v', [None])[0]
            return video_id
        elif parsed_url.netloc == 'youtu.be':
            return parsed_url.path[1:]
        return None
    except Exception as e:
        print(f"Error parsing URL: {e}")
        return None


def get_video_title(video_id):
    """Fetches the title of the YouTube video."""
    try:
        response = youtube.videos().list(
            part="snippet",
            id=video_id
        ).execute()
        title = response['items'][0]['snippet']['title']
        safe_title = re.sub(r'[\/\\:*?"<>|]', '_', title)  # Replace invalid filename characters
        return safe_title
    except Exception as e:
        print(f"Error fetching video title: {e}")
        return "Unknown_Video"


def get_video_comments(video_id):
    """Fetches all top-level comments for a YouTube video."""
    comments = []
    next_page_token = None
    while True:
        try:
            response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=100,
                pageToken=next_page_token,
                textFormat='plainText'
            ).execute()
        except Exception as e:
            print(f"Error fetching comments: {e}")
            return None

        for item in response.get('items', []):
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append([
                comment['authorDisplayName'],
                comment['publishedAt'],
                comment['updatedAt'],
                comment['likeCount'],
                comment['textDisplay']
            ])

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    return comments


def analyze_sentiment(comment_text):
    """Analyzes the sentiment of a comment."""
    try:
        truncated_text = comment_text[:512]
        result = sentiment_pipeline(truncated_text)[0]
        return result['label']
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return "UNKNOWN"


def save_comments_to_csv(comments, video_title):
    """Saves the comments (including duplicates) to a CSV file using the video title as filename."""
    output_file = f"{video_title}.csv"
    columns = ['Author', 'Published At', 'Updated At', 'Like Count', 'Comment', 'Sentiment']

    df = pd.DataFrame(comments, columns=columns)
    df.to_csv(output_file, index=False, encoding='utf-8-sig')

    print(f"Comments with sentiment analysis saved to: {output_file}")


if __name__ == '__main__':
    youtube_url = input("Enter a YouTube video URL: ")
    video_id = get_video_id_from_url(youtube_url)

    if not video_id:
        print("Invalid YouTube URL. Please enter a valid URL.")
    else:
        video_title = get_video_title(video_id)
        comments = get_video_comments(video_id)

        if comments is None:
            print("Failed to retrieve comments.")
        else:
            analyzed_comments = []
            for comment in comments:
                author, published_at, updated_at, like_count, text = comment
                sentiment = analyze_sentiment(text)
                analyzed_comments.append([author, published_at, updated_at, like_count, text, sentiment])

            save_comments_to_csv(analyzed_comments, video_title)
