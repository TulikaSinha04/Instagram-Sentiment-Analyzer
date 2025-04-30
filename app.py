from flask import Flask, render_template, request, redirect, url_for 
from scraper import scrape_instagram_data
from sentiment_utils import analyze_sentiment

app = Flask(__name__)

sentiment_post_map = {
    'Very Positive': [],
    'Positive': [],
    'Neutral': [],
    'Negative': [],
    'Very Negative': []
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    username = request.form['username']
    data = scrape_instagram_data(username)

    sentiments = []
    zipped_data = []

    for i, caption in enumerate(data['captions']):
        hashtags = data['hashtags'][i]
        sentiment = analyze_sentiment(caption, hashtags)  # Analyze sentiment using both caption and hashtags
        sentiments.append(sentiment)

        post_link = data['post_links'][i]

        # Store mapping for filter view
        sentiment_post_map[sentiment].append((caption, post_link))

        # For results view
        zipped_data.append((post_link, caption, hashtags, sentiment))

    result = {
        'username': username,
        'posts': data['posts'],
        'followers': data['followers'],
        'following': data['following'],
        'links': data['post_links'],
        'captions': data['captions'],
        'hashtags': data['hashtags'],
        'sentiments': sentiments
    }

    return render_template('results.html', result=result, zipped=zipped_data)

@app.route('/filter/<mood>')
def filter_by_mood(mood):
    posts = sentiment_post_map.get(mood, [])
    return render_template('filter.html', mood=mood, posts=posts)

if __name__ == '__main__':
    app.run(debug=True)
