from flask import Flask, render_template, jsonify
from rake_nltk import Rake
import openai
from openai import AzureOpenAI

app = Flask(__name__)
rake = Rake()
from dotenv import load_dotenv
import os

load_dotenv()

# Set up the OpenAI API with Azure
# openai.base_url = os.getenv("AZURE_OPENAI_ENDPOINT")
# openai.api_version = "2024-10-21"  
# openai.api_key = os.getenv("AZURE_OPENAPI_KEY")

deployment_name = os.getenv("AZURE_OPENAI_MODEL_NAME")
azure_api_key = os.getenv("AZURE_OPENAPI_KEY")

openai_client = AzureOpenAI(api_key=azure_api_key, azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"), api_version="2024-10-21")

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

@app.route('/process', methods=['POST'])
def process():
    # Make a request (e.g., for text completion)
    response = openai_client.chat.completions.create(
        model=deployment_name,  # Specify the deployment name
        messages=[
            {
                "role": "user",
                "content": """TAPS Journey map:
                    1. Immediate Grief, Shock & Emotion:
                        Overwhelmed, loss of purpose; shock and trauma emotions (isolation) present and challenging to understand
                        Individuals may struggle to deal with family responsibilities alone
                    2. Navigating Family Relationships
                        Experiencing tension between individuals within the family unit; lack of support from family members
                    3. Learning to Process Grief
                        Experiencing grief and learning to process those emotions
                    4. Moments that Matter
                        Renewed experience of grief around anniversaries of loss, holidays, and special moments
                    5. Feeling Immersed, Connected & Seen
                        Finding new purpose and goals to begin moving towards Positive Integration
                    6. New Growth & Purpose
                        Healthy point in grief journey; feeling capable to help others and a desire to do so.""",
            },
        ],
        max_tokens=300
    )

    # Print the result
    print(response.choices[0].message.content.strip())

    return jsonify({'new_journey_map': response.choices[0].message.content.strip()})

@app.route('/distribution')
def distribution():
    return render_template('distribution.html')

if __name__ == '__main__':
    app.run(debug=True)

