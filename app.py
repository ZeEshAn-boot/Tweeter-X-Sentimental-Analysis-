import streamlit as st
import pickle
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import nltk

# Download stopwords once, using Streamlit's caching
@st.cache_resource
def load_stopwords():
    nltk.download('stopwords')
    return stopwords.words('english')

# Load model and vectorizer once
@st.cache_resource
def load_model_and_vectorizer():
    with open('model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('vectorizer.pkl', 'rb') as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)
    return model, vectorizer

# Load the dataset directly into memory for real user lookup
@st.cache_data
def load_dataset():
    try:
        # Standard columns matching the Sentiment140 layout
        df = pd.read_csv(
            'tweeter-dataset.zip', 
            encoding='latin-1', 
            names=['target', 'ids', 'date', 'flag', 'user', 'text']
        )
        df['user'] = df['user'].astype(str).str.strip()
        return df
    except FileNotFoundError:
        st.error("Dataset file ('tweeter-dataset.zip') not found in this folder. Please verify the filename.")
        return None

# Define sentiment prediction function
def predict_sentiment(text, model, vectorizer, stop_words):
    # Preprocess text exactly how the model was trained
    text = re.sub('[^a-zA-Z]', ' ', text)
    text = text.lower()
    text = text.split()
    text = [word for word in text if word not in stop_words]
    text = ' '.join(text)
    text = [text]
    text = vectorizer.transform(text)
    
    # Predict sentiment
    sentiment = model.predict(text)[0]
    return "Negative" if sentiment == 0 else "Positive"

# Function to create a colored card
def create_card(tweet_text, sentiment):
    color = "#d4edda" if sentiment == "Positive" else "#f8d7da"
    text_color = "#155724" if sentiment == "Positive" else "#721c24"
    border_color = "#c3e6cb" if sentiment == "Positive" else "#f5c6cb"
    
    card_html = f"""
    <div style="background-color: {color}; color: {text_color}; padding: 15px; border-radius: 5px; border: 1px solid {border_color}; margin: 10px 0;">
        <strong style="text-transform: uppercase; font-size: 0.85em;">{sentiment} Sentiment</strong>
        <p style="margin-top: 5px; margin-bottom: 0; font-size: 1.05em;">{tweet_text}</p>
    </div>
    """
    return card_html

# Main app logic
def main():
    st.set_page_config(page_title="Twitter Sentiment Analysis", page_icon="📊")
    st.title("Twitter Sentiment Analysis")

    # Load resources
    stop_words = load_stopwords()
    model, vectorizer = load_model_and_vectorizer()
    df = load_dataset()

    # User input UI
    option = st.selectbox("Choose an option", ["Input text", "Get tweets from user"])
    
    if option == "Input text":
        text_input = st.text_area("Enter text to analyze sentiment")
        if st.button("Analyze"):
            if text_input.strip() == "":
                st.warning("Please enter some text before analyzing.")
            else:
                sentiment = predict_sentiment(text_input, model, vectorizer, stop_words)
                
                # Render standalone card layout for text analysis input
                card_html = create_card(text_input, sentiment)
                st.markdown(card_html, unsafe_allow_html=True)

    elif option == "Get tweets from user":
        username = st.text_input("Enter Twitter username")
        if st.button("Fetch Tweets"):
            if username.strip() == "":
                st.warning("Please enter a username first.")
            elif df is None:
                st.error("Database unavailable. Please verify 'tweets.csv' is in your project directory.")
            else:
                # Search dataset for matching user records (case-insensitive)
                matched_tweets = df[df['user'].str.lower() == username.lower().strip()]
                
                if not matched_tweets.empty:
                    # Fetch up to 5 tweets found for this specific username
                    tweets_to_display = matched_tweets['text'].head(5).tolist()
                    st.success(f"Found {len(tweets_to_display)} records for user: @{username}")
                    
                    for tweet_text in tweets_to_display:
                        sentiment = predict_sentiment(tweet_text, model, vectorizer, stop_words)
                        card_html = create_card(tweet_text, sentiment)
                        st.markdown(card_html, unsafe_allow_html=True)
                else:
                    st.info(f"No records found for username '{username}' within the dataset slice.")

if __name__ == "__main__":
    main()