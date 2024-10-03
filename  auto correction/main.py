import nltk
import textdistance
from nltk.corpus import words
nltk.download('words')
word_list = set(words.words())

def get_suggestions(word):

    suggestions = sorted(word_list, key=lambda x: textdistance.levenshtein(word, x))[:5]
    return suggestions

def autocorrect(word):

    if word in word_list:
        return word


    suggestions = get_suggestions(word)
    if suggestions:
        return suggestions[0]
    else:
        return word

def correct_sentence(sentence):

    words = sentence.split()
    corrected_words = [autocorrect(word) for word in words]
    corrected_sentence = ' '.join(corrected_words)
    return corrected_sentence


sentence = input("Enter a sentence to autocorrect: ")
corrected = correct_sentence(sentence)
print("Original:", sentence)
print("Corrected:", corrected)


