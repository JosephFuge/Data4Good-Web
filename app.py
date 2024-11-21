from flask import Flask, render_template
from rake_nltk import Rake

app = Flask(__name__)
rake = Rake()

@app.route('/')
def home():
    text = """Natural language processing (NLP) is a field of artificial intelligence 
    that focuses on the interaction between computers and humans using natural language."""

    # Extract key phrases
    rake.extract_keywords_from_text(text)

    # Get the ranked key phrases
    key_phrases = rake.get_ranked_phrases()
    return render_template('index.html', data=key_phrases[0])

if __name__ == '__main__':
    app.run(debug=True)

