def analyze_sentiment(df):
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    # Function to perform sentiment analysis using VADER
    def get_vader_sentiment(text):
      analyzer = SentimentIntensityAnalyzer()
      sentiment_score = analyzer.polarity_scores(text)
      # We extract the compound score which represents the overall sentiment
      return sentiment_score['compound']
    # Apply sentiment analysis to the 'translated_text' column
    df['vader_sentiment'] = df['translated_text'].apply(get_vader_sentiment)
    return df