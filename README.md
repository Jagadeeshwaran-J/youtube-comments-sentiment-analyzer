# 📺 YouTube Comments Sentiment Analyzer

This project is a **Python tool** that fetches comments from a YouTube video and analyzes the **sentiment** of each comment (Positive / Negative / Neutral) using a Hugging Face model.  
The results are saved in a **CSV file** with the video title as the filename.

---

## ✨ What this project does
1. You give a **YouTube video link**.  
2. The script connects to **YouTube Data API v3** and downloads all top-level comments.  
3. Each comment is passed to an **AI sentiment analysis model**.  
4. The analyzed comments are saved into a **CSV file**.  

This is useful for:
- Understanding audience reactions to a video.  
- Collecting feedback for research.  
- Learning how to combine **APIs** and **AI/NLP**.  

---

## 🛠️ Requirements

- Python **3.8 or above**
- A **YouTube Data API v3 key** from Google Cloud
- Libraries listed in `requirements.txt`

### Install dependencies
```bash
pip install -r requirements.txt
```

---

## 📦 Setup

### 1. Clone or download this project
```bash
git clone https://github.com/yourusername/youtube-comments-sentiment.git
cd youtube-comments-sentiment
```

### 2. Create a virtual environment (optional but recommended)
```bash
python -m venv .venv
.\.venv\Scriptsctivate   # On Windows
source .venv/bin/activate # On Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## 🔑 Get Your YouTube API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/).  
2. Create a **new project** (or use an existing one).  
3. Enable **YouTube Data API v3**.  
4. Go to **APIs & Services → Credentials → Create API Key**.  
5. Copy the API Key.  

Replace the key in the script:
```python
API_KEY = "YOUR_NEW_API_KEY"
```

---

## ▶️ How to Run

Run the script from your terminal:
```bash
python Youtube.py
```

You will be asked to paste a YouTube video URL:
```
Enter a YouTube video URL: https://www.youtube.com/watch?v=cp0_xWxLGaI
```

The script will:
- Get the video title  
- Download all comments  
- Analyze each comment’s sentiment  
- Save results into a CSV file  

---

## 📂 Example Output

**CSV file name**: `My_Awesome_Video.csv`

| Author     | Published At       | Like Count | Comment                 | Sentiment |
|------------|-------------------|------------|-------------------------|-----------|
| John Doe   | 2025-08-10 12:34  | 15         | Great video! 👏         | POSITIVE  |
| Jane Smith | 2025-08-10 14:12  | 3          | Not helpful at all 😕    | NEGATIVE  |

---

## ⚠️ Notes

- The script only fetches **top-level comments** (not replies).  
- Each comment is trimmed to **512 characters** before sentiment analysis.  
- If you see a 403 Forbidden error with a message like "Requests to this API youtube method... are blocked," your API key is likely restricted. To fix this, go to your Google Cloud Console, navigate to APIs & Services > Credentials, select your API key, and ensure that API restrictions are set to YouTube Data API v3 and that there are no application restrictions that would prevent your script from running.
- The Hugging Face model used is [tabularisai/multilingual-sentiment-analysis](https://huggingface.co/tabularisai/multilingual-sentiment-analysis).

---
