from textblob import TextBlob

def analyze_sentiment(text, hashtags=None):
    # Start by analyzing the sentiment of the caption
    polarity = TextBlob(text).sentiment.polarity

    # Modify sentiment based on hashtags
    if hashtags:
        for hashtag in hashtags:
            # Consider sentiment of the hashtag text itself
            hashtag_sentiment = TextBlob(hashtag).sentiment.polarity
            # Adjust overall sentiment based on hashtag sentiment
            if hashtag_sentiment > 0:
                polarity += 0.1  # Positive hashtag, increase positivity
            elif hashtag_sentiment < 0:
                polarity -= 0.1  # Negative hashtag, increase negativity

    # Determine the sentiment category based on adjusted polarity
    if polarity >= 0.5:
        return 'Very Positive'
    elif 0.1 <= polarity < 0.5:
        return 'Positive'
    elif -0.1 < polarity < 0.1:
        return 'Neutral'
    elif -0.5 <= polarity <= -0.1:
        return 'Negative'
    else:
        return 'Very Negative'

def calculate_engagement(followers, likes, comments):
    try:
        followers = int(followers.replace('k','000').replace('m','000000').replace(',',''))
        return round(((likes + comments) / followers) * 100, 2)
    except:
        return 0.0
