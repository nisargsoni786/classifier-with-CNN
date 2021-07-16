from rasa.nlu.components import Component
from rasa.nlu import utils
from rasa.nlu.model import Metadata
from mtranslate import translate

import nltk

nltk.downloader.download('vader_lexicon')

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os

class SentimentAnalyzer(Component):
    """A pre-trained sentiment component"""

    name = "sentiment_analyzer"
    provides = ["entities"]
    requires = []
    defaults = {}
    language_list = ["en"]



    @classmethod
    def required_packages(cls):
        return ["nltk"]
    
    def __init__(self, component_config=None):
        super(SentimentAnalyzer, self).__init__(component_config)


    
    def train(self, training_data, cfg, **kwargs):
        """Not needed, because the the model is pretrained"""
        pass



    def convert_to_rasa(self, value, confidence):
        """Convert model output into the Rasa NLU compatible output format."""
        
        entity = {"value": value,
                  "confidence": confidence,
                  "entity": "sentiment",
                  "extractor": "sentiment_extractor"}

        return entity


    def process(self, message, **kwargs):
        try:
            """Retrieve the text message, pass it to the classifier
            and append the prediction results to the message class."""
            print(message.data['text'])
            sid = SentimentIntensityAnalyzer()
            texts=translate(message.data['text']).lower()
            print('texts',texts)
            res = sid.polarity_scores(texts)
            print('res',res)
            key, value = max(res.items(), key=lambda x: x[1])
            print('key',key)
            print('value',value)

            entity = self.convert_to_rasa(key, value)

            message.set("entities", [entity], add_to_output=True)
        
        except Exception as e:
            print('\n\n',e,'\n\n')

    # def persist(self, model_dir):
    #     """Pass because a pre-trained model is already persisted"""
    #     pass