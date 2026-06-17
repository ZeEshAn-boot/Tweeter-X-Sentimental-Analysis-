Twitter Sentiment Analysis System

A machine learning-based web application that analyzes the sentiment of tweets and classifies them as Positive or Negative using Natural Language Processing (NLP) and Logistic Regression. The project includes a complete model training pipeline and an interactive Streamlit web application for real-time predictions. The system achieves approximately 70.4% accuracy on the test dataset.

🚀 Features
✅ Real-time sentiment analysis for custom text input
✅ Twitter user tweet lookup from dataset
✅ NLP preprocessing pipeline
✅ TF-IDF vectorization
✅ Logistic Regression classifier
✅ Interactive Streamlit interface
✅ Cached model loading for improved performance
✅ Saved model and vectorizer using Pickle
🏗️ Project Architecture
Raw Twitter Dataset
        │
        ▼
Text Cleaning & Preprocessing
(Regex + Stopword Removal + Stemming)
        │
        ▼
TF-IDF Vectorization
        │
        ▼
Logistic Regression Training
        │
        ▼
Export Model Files
(model.pkl & vectorizer.pkl)
        │
        ▼
Streamlit Web Application
(app.py)

The system consists of two main components: a model training pipeline and a Streamlit web interface.

📂 Project Structure
Twitter-Sentiment-Analysis/
│
├── app.py
├── sentimental-analysis.ipynb
├── model.pkl
├── vectorizer.pkl
├── tweeter-dataset.zip
├── requirements.txt
└── README.md
🛠️ Technologies Used
Python
Streamlit
Scikit-Learn
NLTK
Pandas
NumPy
Pickle
Regular Expressions (Regex)
🔍 NLP Preprocessing Steps

The text preprocessing pipeline performs:

Removal of special characters using Regex
Conversion to lowercase
Tokenization
Stopword removal
Porter Stemming

Example:

"Studying", "Studies", "Studied"
        ↓
      "studi"

This normalization improves model performance by reducing word variations.

📊 Dataset
Dataset contains positive and negative tweets.
2,500 positive tweets and 2,500 negative tweets were selected to create a balanced dataset of 5,000 samples.
Target labels:
0 → Negative
1 → Positive
🧠 Machine Learning Model
Feature Extraction
vectorizer = TfidfVectorizer()

TF-IDF converts text into numerical vectors suitable for machine learning. The vectorizer is fitted only on training data to prevent data leakage.

Classification Model
model = LogisticRegression(max_iter=1000)

The model was trained with:

Train/Test Split: 80/20
Stratified Sampling
Random State: 42

These settings ensure reproducibility and balanced class distribution.

📈 Model Performance
Metric	Value
Accuracy	70.40%

The trained Logistic Regression model achieved approximately 70.4% testing accuracy.

💾 Model Serialization

After training, the model and vectorizer are stored as:

model.pkl
vectorizer.pkl

These files are loaded by the Streamlit application for inference.

🌐 Streamlit Web Application
Mode 1: Input Text

Users can enter any text and receive sentiment predictions instantly.

Example:

Input:
"I am absolutely thrilled with this new development stack!"

Output:
POSITIVE SENTIMENT
Input:
"This product is completely broken."

Output:
NEGATIVE SENTIMENT

The application provides color-coded sentiment responses.

Mode 2: User Tweet Lookup

Users can search tweets by username from the dataset and view sentiment predictions for retrieved tweets. The application displays up to five matching records.

Example:

Username: scotthamilton

Found 5 records
Tweet 1 → Negative
Tweet 2 → Negative
...
⚡ Performance Optimization

The Streamlit application uses:

@st.cache_resource
@st.cache_data

to cache models and datasets in memory, improving execution speed and reducing repeated file loading.

🚀 Installation
Clone Repository
git clone https://github.com/your-username/twitter-sentiment-analysis.git
cd twitter-sentiment-analysis
Create Virtual Environment
python -m venv venv

Activate environment:

Windows

venv\Scripts\activate

Linux / Mac

source venv/bin/activate
Install Dependencies
pip install -r requirements.txt
▶️ Run Application
streamlit run app.py

Open browser:

http://localhost:8501
📌 Future Improvements
Add Neutral sentiment class
Use deep learning models (LSTM/BERT)
Live Twitter API integration
Real-time tweet streaming
Sentiment visualization dashboards
👨‍💻 Author

Muhammad Zeeshan

AI Automation Engineer | Machine Learning Enthusiast | NLP Developer

LinkedIn: https://www.linkedin.com/in/muhammad-zeeshan-1a9b32261/
