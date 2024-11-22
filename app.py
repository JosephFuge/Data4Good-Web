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

@app.route('/journeymap')
def journeymap():
    # Extract key phrases
    # rake.extract_keywords_from_text(text)

    # Get the ranked key phrases
    # key_phrases = rake.get_ranked_phrases()
    return render_template('journeymap.html', current_journey_map="fake journey map testing")

@app.route('/survey')
def survey():
    # Extract key phrases
    # rake.extract_keywords_from_text(text)

    # Get the ranked key phrases
    # key_phrases = rake.get_ranked_phrases()
    return render_template('survey.html')

@app.route('/survey-results')
def survey_results():
    return render_template('survey-results.html')

@app.route('/distribution')
def distribution():
    return render_template('distribution.html')

if __name__ == '__main__':
    app.run(debug=True)

