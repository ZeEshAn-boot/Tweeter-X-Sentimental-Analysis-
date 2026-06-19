# Twitter Sentiment Analysis System

A Machine Learning and NLP-based web application that analyzes tweets and classifies them into **Positive** or **Negative** sentiments using **Logistic Regression** and **TF-IDF Vectorization**.

---

## 🚀 Features

- Real-time sentiment analysis for custom text input
- Twitter user tweet lookup from dataset
- Natural Language Processing (NLP) pipeline
- TF-IDF feature extraction
- Logistic Regression classifier
- Interactive Streamlit web application
- Cached model loading for improved performance
- Saved model and vectorizer using Pickle

---

## 🏗️ System Architecture

```text
Raw Twitter Dataset
        │
        ▼
Text Preprocessing
(Regex + Stopword Removal + Stemming)
        │
        ▼
TF-IDF Vectorization
        │
        ▼
Logistic Regression Model
        │
        ▼
Save Model (model.pkl)
Save Vectorizer (vectorizer.pkl)
        │
        ▼
Streamlit Web Application
```

---

## 📂 Project Structure

```text
Twitter-Sentiment-Analysis/
│
├── app.py
├── sentimental-analysis.ipynb
├── model.pkl
├── vectorizer.pkl
├── tweeter-dataset.zip
├── requirements.txt
└── README.md
```

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Scikit-Learn
- NLTK
- Pandas
- NumPy
- Pickle
- Regular Expressions (Regex)

---

## 🔍 NLP Preprocessing

The preprocessing pipeline includes:

- Removing special characters using Regex
- Converting text to lowercase
- Tokenization
- Stopword removal
- Porter Stemming

Example:

```python
"studying" → "studi"
"studies"  → "studi"
"studied"  → "studi"
```

---

## 📊 Dataset

- Balanced dataset containing:
  - 2,500 Positive tweets
  - 2,500 Negative tweets
- Total: **5,000 tweets**

Target labels:

- `0` → Negative
- `1` → Positive

---

## 🧠 Machine Learning Model

### Feature Extraction

```python
vectorizer = TfidfVectorizer()
```

### Classification Model

```python
model = LogisticRegression(max_iter=1000)
```

### Training Configuration

- Train/Test Split: **80/20**
- Stratified Sampling
- Random State: **42**

---

## 📈 Model Performance

| Metric | Score |
|--------|-------|
| Accuracy | **70.40%** |

---

## 💾 Saved Files

```text
model.pkl
vectorizer.pkl
```

These files are loaded by the Streamlit application for prediction.

---

## 🌐 Streamlit Application

### Mode 1: Input Text

Example:

**Input:**

```text
I am absolutely thrilled with this new development stack!
```

**Output:**

```text
POSITIVE SENTIMENT
```

---

### Mode 2: Twitter User Search

Search tweets by username from the dataset and view sentiment predictions.

Example:

```text
Username: scotthamilton
Found 5 tweets
```

---

## ⚡ Performance Optimization

The application uses Streamlit caching:

```python
@st.cache_resource
@st.cache_data
```

This improves loading speed and avoids repeated file processing.

---

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/ZeEshAn-boot/Tweeter-X-Sentimental-Analysis-.git
cd Tweeter-X-Sentimental-Analysis-
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / Mac**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 📥 Prepare TweetClaw Exports

The user search mode can load a local `tweets.csv` file. Use
`scripts/prepare_tweetclaw_dataset.py` to convert reviewed TweetClaw JSON,
JSONL, or CSV exports into the Sentiment140-style columns expected by `app.py`.

```bash
python scripts/prepare_tweetclaw_dataset.py examples/tweetclaw_export.jsonl \
  --output tweets.csv
```

Review exports before conversion. Do not commit private account data,
credentials, or non-public tweets. TweetClaw is available from
https://github.com/Xquik-dev/tweetclaw.

---

## ▶️ Run Application

```bash
streamlit run app.py
```

Open in browser:

```text
http://localhost:8501
```

---

## 🔮 Future Improvements

- Add Neutral sentiment detection
- Integrate Twitter API
- Use Deep Learning models (LSTM/BERT)
- Real-time tweet streaming
- Interactive dashboards

---

## 👨‍💻 Author

**Muhammad Zeeshan**

AI Automation Engineer | Machine Learning Enthusiast | NLP Developer

LinkedIn:
https://www.linkedin.com/in/muhammad-zeeshan-1a9b32261/

---

## 📜 License

This project is licensed under the MIT License.

⭐ If you like this project, don't forget to star the repository!
