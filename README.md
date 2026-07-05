# 🎥 YouTube Content Analyzer & Downloader

A machine learning-based Flask application that analyzes YouTube video metadata and predicts video categories using NLP techniques.

![Python](https://img.shields.io/badge/Python-3670A0?style=flat&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)

---

## 📖 Overview

YouTube Content Analyzer extracts a video's metadata (title, description, tags), vectorizes the text using TF-IDF, and classifies its category using a trained Naive Bayes model — all through an interactive Flask dashboard. It also supports downloading videos via `yt-dlp`.

---

## ✨ Features

- YouTube video metadata extraction
- Video category prediction via ML
- TF-IDF text vectorization
- Naive Bayes classification model
- Video downloading using yt-dlp
- Interactive web dashboard

---

## 🛠️ Tech Stack

| Layer          | Technology              |
|-----------------|---------------------------|
| Backend         | Python, Flask              |
| ML              | Scikit-learn, TF-IDF, Naive Bayes |
| Video handling  | yt-dlp                     |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- pip

### Installation
```bash
git clone https://github.com/areebaathar-dev/youtube-content-analyzer.git
cd youtube-content-analyzer
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Then open `http://localhost:5000` in your browser.

---

## 🧠 ML Model

- **Vectorization:** TF-IDF on video title, description, and tags
- **Classifier:** Multinomial Naive Bayes
- **Output:** Predicted video category with confidence score

---

## 📁 Project Structure
youtube-content-analyzer/
├── app.py            # Flask app entry point
├── model/            # Trained ML model & vectorizer
├── static/           # CSS, JS
├── templates/        # HTML templates
└── requirements.txt


---

## 📸 Screenshots

### Dashboard
<img width="1689" height="961" alt="image" src="https://github.com/user-attachments/assets/2d00646a-dc5a-4494-b870-6482608c8c3b" />
<img width="1658" height="935" alt="image" src="https://github.com/user-attachments/assets/5ce57052-21ac-4d69-b664-fe8db49e31e6" />

---

## 🔭 Future Improvements

- Deep learning-based classification (e.g. BERT embeddings)
- Batch analysis for multiple videos at once
- Deploy live demo on Render/Heroku

---

## 📄 License

This project is licensed under the MIT License.

---

## 👩‍💻 Author

**Areeba Athar**
[LinkedIn](https://linkedin.com/in/areeba-athar) · [GitHub](https://github.com/areebaathar-dev)
