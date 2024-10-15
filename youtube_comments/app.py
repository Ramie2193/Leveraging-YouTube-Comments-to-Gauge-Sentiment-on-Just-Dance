import eel
from pymongo import MongoClient
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize Eel
eel.init("web")

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['youtube_comments']
collection = db['comments']

# Custom sentiment analysis function
def custom_sentiment_analysis(text):
    positive_words = ["love", "amazing", "fun", "excellent", "great"]
    negative_words = ["boring", "disappointed", "poor", "bad", "terrible"]
    
    text = text.lower()
    positive_score = sum(word in text for word in positive_words)
    negative_score = sum(word in text for word in negative_words)
    
    if positive_score > negative_score:
        return 1  # Positive
    elif negative_score > positive_score:
        return -1  # Negative
    else:
        return 0  # Neutral

# Function to perform sentiment analysis
def analyze_sentiment(text):
    # Using TextBlob
    blob = TextBlob(text)
    textblob_sentiment = blob.sentiment.polarity

    # Using VADER
    analyzer = SentimentIntensityAnalyzer()
    vader_sentiment = analyzer.polarity_scores(text)['compound']

    # Using Custom Algorithm
    custom_sentiment = custom_sentiment_analysis(text)

    # Determine the best sentiment
    best_algorithm = "Custom"
    best_sentiment = "Neutral"
    if abs(textblob_sentiment) > abs(vader_sentiment) and abs(textblob_sentiment) > abs(custom_sentiment):
        best_algorithm = "TextBlob"
        best_sentiment = "Positive" if textblob_sentiment > 0 else "Negative"
    elif abs(vader_sentiment) > abs(textblob_sentiment) and abs(vader_sentiment) > abs(custom_sentiment):
        best_algorithm = "VADER"
        best_sentiment = "Positive" if vader_sentiment > 0 else "Negative"
    else:
        best_sentiment = "Positive" if custom_sentiment == 1 else "Negative" if custom_sentiment == -1 else "Neutral"

    return {
        "textblob": textblob_sentiment,
        "vader": vader_sentiment,
        "custom": custom_sentiment,
        "best_algorithm": best_algorithm,
        "best_sentiment": best_sentiment
    }

# Expose the function to JavaScript
@eel.expose
def save_comment(comment):
    sentiment = analyze_sentiment(comment)
    # Save to MongoDB
    collection.insert_one({"comment": comment, "sentiment": sentiment})
    return sentiment

# Start Eel with the main HTML file
eel.start("index.html")