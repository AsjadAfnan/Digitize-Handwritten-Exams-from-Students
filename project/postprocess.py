import spacy
from hunspell import Hunspell

def correct_text(text):
    nlp = spacy.load("de_core_news_sm")
    hspell = Hunspell("de_DE")
    
    corrected_words = []
    for token in nlp(text):
        if not hspell.spell(token.text):
            suggestions = hspell.suggest(token.text)
            corrected = suggestions[0] if suggestions else token.text
            corrected_words.append(corrected)
        else:
            corrected_words.append(token.text)
    
    return " ".join(corrected_words)