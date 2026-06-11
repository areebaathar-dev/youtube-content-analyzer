from flask import Flask, request, jsonify, send_from_directory, render_template
import yt_dlp
import os
import uuid
import threading
import pandas as pd
import re
import random

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

app = Flask(__name__)

# -----------------------------
# FOLDERS
# -----------------------------
DOWNLOAD_FOLDER = "downloads"
REPORTS_FOLDER = "reports"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORTS_FOLDER, exist_ok=True)

tasks = {}

# -----------------------------
# DATASET + PREPROCESSING
# -----------------------------
data = pd.read_csv("dataset.csv")

data.dropna(inplace=True)
data.drop_duplicates(inplace=True)

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

data["text"] = data["text"].apply(clean_text)

texts = data["text"]
labels = data["label"]

# -----------------------------
# TRAIN MODEL
# -----------------------------
vectorizer = TfidfVectorizer(stop_words="english")

X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.2, random_state=42
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = MultinomialNB()
model.fit(X_train_vec, y_train)

y_pred = model.predict(X_test_vec)

accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", round(accuracy * 100, 2), "%")

# -----------------------------
# METRICS
# -----------------------------
def viral_score(views, likes):
    return round((likes / views) * 100, 2) if views else 0

def engagement_score(views, likes):
    return round((likes / views) * 120, 2) if views else 0

def trending_score(v, e):
    return round((v * 0.7) + (e * 0.3), 2)

def best_time(category):
    return {
        "News": "8 AM - 10 AM",
        "Education": "6 PM - 9 PM",
        "Entertainment": "7 PM - 11 PM",
        "Sports": "5 PM - 8 PM"
    }.get(category, "7 PM - 9 PM")

# -----------------------------
# AI FUNCTIONS
# -----------------------------
def ai_suggestion(v, e, title):
    if v < 4:
        return "Improve thumbnail and visual impact."
    if e < 4:
        return "Add strong hook in first 3 seconds."
    return "Good performance, maintain consistency."

def ai_explanation(v, e):
    if v < 4:
        return "Low viral performance due to weak engagement."
    if e < 4:
        return "Engagement is low compared to views."
    return "Performance is balanced and stable."

def content_coach(v, e):
    if v < 5:
        return "Improve title and thumbnail strategy."
    return "Content strategy is strong."

def generate_seo_tags(title):
    return list(set(title.lower().split()[:6])) if title else []

def thumbnail_score(views, likes):
    if not views:
        return 0
    score = (likes / views) * 50
    return round(min(score, 10), 1)

def copyright_risk(title):
    keywords = ["movie", "song", "reupload", "tiktok", "clip"]
    return 80 if any(k in title.lower() for k in keywords) else 0

# -----------------------------
# PDF REPORT
# -----------------------------
def generate_pdf_report(task_id, data_dict):

    file_path = os.path.join(REPORTS_FOLDER, f"{task_id}.pdf")
    c = canvas.Canvas(file_path, pagesize=letter)

    y = 750

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "YouTube AI Report")

    y -= 40
    c.setFont("Helvetica", 12)

    for key, value in data_dict.items():
        c.drawString(50, y, f"{key}: {value}")
        y -= 20

    c.save()

# -----------------------------
# VIDEO PROCESSING
# -----------------------------
def process_video(task_id, url):

    try:
        tasks[task_id]["status"] = "Fetching..."

        with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
            info = ydl.extract_info(url, download=False)

        title = info.get("title", "")
        views = info.get("view_count", 0)
        likes = info.get("like_count", 0)

        category = model.predict(vectorizer.transform([clean_text(title)]))[0]

        v = viral_score(views, likes)
        e = engagement_score(views, likes)
        t = trending_score(v, e)

        # ✅ FULL FIXED RESULT (NO MISSING KEYS)
        result = {
            "title": title,
            "views": views,
            "likes": likes,
            "category": category,
            "viral_score": v,
            "engagement": e,
            "trending": t,
            "best_time": best_time(category),

            # UI FIXED FIELDS
            "seo_tags": generate_seo_tags(title),
            "thumbnail_score": thumbnail_score(views, likes),

            # AI FEATURES
            "suggestion": ai_suggestion(v, e, title),
            "coach": content_coach(v, e),
            "explanation": ai_explanation(v, e),

            "copyright": copyright_risk(title),
            "accuracy": round(accuracy * 100, 2)
        }

        tasks[task_id].update(result)

        tasks[task_id]["status"] = "Downloading..."

        filename = f"{uuid.uuid4()}.mp4"
        path = os.path.join(DOWNLOAD_FOLDER, filename)

        with yt_dlp.YoutubeDL({"outtmpl": path, "format": "mp4/best"}) as ydl:
            ydl.download([url])

        tasks[task_id]["file"] = filename
        tasks[task_id]["status"] = "Completed"

        # PDF GENERATION
        generate_pdf_report(task_id, result)

    except Exception as e:
        tasks[task_id]["status"] = f"Error: {str(e)}"

# -----------------------------
# ROUTES
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    url = request.json.get("url")
    task_id = str(uuid.uuid4())

    tasks[task_id] = {"status": "Starting..."}

    threading.Thread(target=process_video, args=(task_id, url)).start()

    return jsonify({"task_id": task_id})

@app.route("/status/<task_id>")
def status(task_id):
    return jsonify(tasks.get(task_id, {}))

@app.route("/file/<filename>")
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

@app.route("/report/<task_id>")
def download_report(task_id):
    return send_from_directory(REPORTS_FOLDER, f"{task_id}.pdf", as_attachment=True)

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    print("🚀 Running AI Project")
    print("Accuracy:", round(accuracy * 100, 2), "%")
    app.run(debug=True)