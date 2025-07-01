from utils import apply_leetspeak
import nltk
from nltk.corpus import words

try:
    nltk.data.find('corpora/words')
except LookupError:
    nltk.download('words')

def generate_wordlist(name, pet, year):
    base_words = [name, pet]
    patterns = []

    for word in base_words:
        patterns.extend([
            word.lower(),
            word.capitalize(),
            word + year,
            apply_leetspeak(word),
            apply_leetspeak(word + year)
        ])

    english_words = set(w.lower() for w in words.words())
    patterns = [w for w in patterns if w.lower() in english_words or len(w) > 3]

    return list(set(patterns))