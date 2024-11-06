from pydantic import BaseModel
import re
import emoji
import emot
import hunspell
from app.main import stopwords_es
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from app.infrastructure.utils import get_drive_url_from_file_id
from app.main import spanish_peruvian_dictionary
from app.main import stemmer
import spacy
from typing import List

class Message(BaseModel):
    message: str
    tokens: List[str]

    def process(self, technique):
        self.correct_spelling()
        self.add_space_around_emojis()
        self.add_space_around_emoticons()
        self.emoji_to_description()
        self.emoticon_to_description()
        self.lower()
        self.remove_tags()
        self.remove_mentions()
        self.remove_urls()
        self.remove_numbers()
        self.remove_punctuation()
        self.remove_extra_spaces()
        self.remove_extra_characters()
        self.tokenize()
        self.translate_peruvian_words()
        self.remove_stop_words()
        if technique == "lematización":
            self.lematize()
        else:
            self.stem()
        return self.message

    def correct_spelling(self):
        hs = hunspell.HunSpell('/usr/share/hunspell/es_PE.dic', '/usr/share/hunspell/es_PE.aff')
        palabras = self.message.split()
        texto_corregido = []
        for palabra in palabras:
            correccion = hs.suggest(palabra)
            texto_corregido.append(correccion[0] if correccion else palabra)
        self.message = ' '.join(texto_corregido)
        return self
    
    def add_space_around_emojis(self):
        pattern = f"({'|'.join(map(re.escape, emoji.EMOJI_DATA.keys()))})"
        self.message = re.sub(pattern, r' \1 ', self.message)
        return self

    def add_space_around_emoticons(self):
        pattern = f"({'|'.join(map(re.escape, emot.EMOTICONS_EMO.keys()))})"
        self.message = re.sub(pattern, r' \1 ', self.message)
        return self

    def emoji_to_description(self):
        self.message = emoji.replace_emoji(
            self.message, 
            replace=lambda chars, data_dict: ' '.join(data_dict['es'].split('_')).strip(':')
        )
        return self

    def emoticon_to_description(self):
        emot_obj = emot.core.emot()
        info_emoticonos = emot_obj.emoticons(self.message)
        
        for ubicaciones, significados in zip(info_emoticonos['location'], info_emoticonos['mean']):
            significados = GoogleTranslator(source='en', target='es').translate(text=significados).lower()
            self.message = f"{self.message[:ubicaciones[0]]}{significados}{self.message[ubicaciones[1]:]}"
            info_emoticonos = emot_obj.emoticons(self.message)
        return self

    def lower(self):
        self.message = self.message.lower()
        return self

    def remove_tags(self):
        self.message = re.sub(r'#\w+', '', self.message)
        return self

    def remove_mentions(self):
        self.message = re.sub(r'@\w+', '', self.message)
        return self

    def remove_urls(self):
        self.message = re.sub(r'http\S+', '', self.message)
        return self

    def remove_numbers(self):
        self.message = re.sub(r'\d+', '', self.message)
        return self

    def remove_punctuation(self):
        self.message = re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s]', '', self.message)
        return self

    def remove_extra_spaces(self):
        self.message = re.sub(r'[\r\t\n]', ' ', self.message)
        self.message = re.sub(r'\s{2,}', ' ', self.message).strip()
        return self

    def remove_extra_characters(self):
        allowed_words = {'rr', 'll', 'cc', 'ee', 'oo'}
        patron = re.compile(r'(\w)\1+')

        def replace(match):
            char = match.group(1)
            repetition = match.group(0)
            return char * 2 if char * 2 in allowed_words and len(repetition) > 2 else char
        
        self.message = patron.sub(replace, self.message)
        return self

    def tokenize(self):
        tokens = word_tokenize(self.message, language='spanish')
        self.tokens = [word for word in tokens]
        return self
    
    def translate_peruvian_words(self):
        self.tokens = [spanish_peruvian_dictionary.get(word, word) for word in self.tokens]
        return self

    def remove_stop_words(self):
        self.tokens = [word for word in self.tokens if word.lower() not in stopwords_es]
        return self
    
    def lematize(self):
        self.message = ' '.join([nlp(word)[0].lemma_ for word in self.tokens])
        return self
    
    def stem(self):
        self.message = ' '.join([stemmer.stem(word) for word in self.tokens])