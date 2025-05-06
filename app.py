from flask import Flask, render_template, request
from newspaper import Article
from textblob import TextBlob

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = {}

    if request.method == 'POST':
        url = request.form['url'].strip()
        article = Article(url)

        try:
            article.download()
            article.parse()
            article.nlp()

            analysis = TextBlob(article.text)
            sentiment = "positive" if analysis.polarity > 0 else "negative" if analysis.polarity < 0 else "neutral"

            data = {
                "title": article.title,
                "authors": ', '.join(article.authors) if article.authors else "Unknown",
                "publish_date": article.publish_date if article.publish_date else "Unknown",
                "summary": article.summary,
                "sentiment": f"Polarity: {analysis.polarity:.2f} Sentiment: {sentiment}",
                "url": url
            }

        except Exception as e:
            data = {"error": str(e)}

    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
