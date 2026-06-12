import emoji
import fr_core_news_sm
from spacy.lang.fr.stop_words import STOP_WORDS as stopwords


class SentimentService:

    def __init__(self):
        self.nlp = fr_core_news_sm.load()

    def preprocess_text(self, text):
        text = emoji.demojize(text, language="fr")
        text = text.replace(":", " ")
        text = text.replace("_", " ")
        text = " ".join(text.split())

        doc = self.nlp(text)

        tokens = [
            token.text.lower()
            for token in doc
            if not token.is_punct
            and not token.is_space
        ]
        return " ".join(tokens)