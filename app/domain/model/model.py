import joblib
from urllib.request import urlopen

class Model:
    def __init__(self, url: str):
        self.model_joblib = joblib.load(urlopen(url))

    def predict(self, message):
        return self.model_joblib.predict([message])