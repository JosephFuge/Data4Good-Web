from flask import Flask, render_template, jsonify
from openai import AzureOpenAI
from dotenv import load_dotenv
from services.text_processing import TextProcessor
import csv
import os

load_dotenv()

app = Flask(__name__)

deployment_name = os.getenv("AZURE_OPENAI_MODEL_NAME")
azure_api_key = os.getenv("AZURE_OPENAPI_KEY")
openai_client = AzureOpenAI(api_key=azure_api_key, azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"), api_version="2024-10-21")

csv_path = "TAPS_Cleaned_CSV.csv"
description_column = "Logs.Description"
sort_column = "Logs.LogDate"

key_phrases = []

def get_key_phrases():
    if len(key_phrases) > 0:
        return key_phrases

    recent_logs = 100
    with open(csv_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        # Extract values from the specified column
        column_values = [(row[sort_column], row[description_column]) for row in reader]

    if recent_logs > 0:
        column_values.sort(key=lambda val: val[0])

        column_descriptions = [val[1] for val in column_values[0:50]]
    else:
        column_descriptions = [val[1] for val in column_values]

    tp = TextProcessor()
    emotional_words = [sentiment['text'] for sentiment in tp.sentiment_extremes(column_descriptions, high_thresh=0.95, low_thresh=0.05)]

    key_words = tp.extract_keywords_from_list(emotional_words)
    key_words = key_words[0:10]

    return key_words

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/journeymap')
def journeymap():
    key_phrases = get_key_phrases()
    return render_template('journeymap.html', current_journey_map="""
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
                        Healthy point in grief journey; feeling capable to help others and a desire to do so.""", keywords=', '.join(key_phrases))

@app.route('/survey')
def survey():
    return render_template('survey.html')

@app.route('/survey-results')
def survey_results():
    return render_template('survey-results.html')

@app.route('/process', methods=['POST'])
def process():
    key_phrases = get_key_phrases()
    response = openai_client.chat.completions.create(
        model=deployment_name,  # Specify the deployment name
        messages=[
            {
                "role": "user",
                "content": f"""Given the previous TAPS Journey map, which is meant to help TAPS employees identify where a given person is in their grief journey following the death of a family member or friend who was a current or former member of the military, and then a list of keywords which are appearing more often in conversations between TAPS employees and survivors, generate a new TAPS journey map to account for adapting needs:
                <Journey Map>
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
                        Healthy point in grief journey; feeling capable to help others and a desire to do so.
                </Journey Map>
                <Keywords>
                    {key_phrases}
                </Keywords>

                New journey map:
                """,
            },
        ],
        max_tokens=300
    )

    tp = TextProcessor()

    response_text = tp.replace_asterisks_with_bold(response.choices[0].message.content.strip())

    return jsonify({'new_journey_map': response_text})

@app.route('/stage2-details')
def stage2_details():
    return render_template('stage2-details.html')

@app.route('/distribution')
def distribution():
    return render_template('distribution.html')

if __name__ == '__main__':
    app.run(debug=True)

