from rake_nltk import Rake
from nltk.sentiment import SentimentIntensityAnalyzer
import re

rake = Rake()

class TextProcessor:
    @staticmethod
    def replace_asterisks_with_bold(text_input):
        return re.sub(r'\*\*(.*?)\*\*', r'<br><b>\1</b>', text_input)

    @staticmethod
    def extract_keywords_from_list(inputs):
        rake = Rake()
        result = []
        for text in inputs:
            rake.extract_keywords_from_text(text)
            key_phrases = rake.get_ranked_phrases()
            result.extend(key_phrases)

        return result
        
    @staticmethod
    def sentiment_extremes(phrases, low_thresh=0.2, high_thresh=0.8):
        # Initialize the analyzer
        sia = SentimentIntensityAnalyzer()

        sentiments = []

        high_sentiments = 0
        low_sentiments = 0
        for p in phrases:
            sentiment = sia.polarity_scores(p)
            sentiment['text'] = p
            if sentiment['compound'] <= low_thresh:
                low_sentiments = low_sentiments + 1
                sentiments.append(sentiment)
            elif sentiment['compound'] >= high_thresh:
                high_sentiments = high_sentiments + 1
                sentiments.append(sentiment)

        print(f'high: {high_sentiments} low: {low_sentiments}')
        # print(sentiments)

        return sentiments

