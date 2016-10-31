from __future__ import print_function, unicode_literals
import random, logging, os, json, config
os.environ['NLTK_DATA'] = os.getcwd() + '/nltk_data'
from textblob import TextBlob

def preprocess_text(text):
    # 1. Convert all to lowercase for simplicity
    # 2. Ensure that there is only one sentence
    return text.lower().replace(".", " ")

def check_for_greeting(sentence):
    """If any of the words in the user's input was a greeting, return a greeting response"""
    for word in sentence.words:
        if word in config.GREETING_KEYWORDS:
            return random.choice(config.GREETING_RESPONSES)
    return ''

def interpret(text):
    sentence = preprocess_text(text)
    parsed = TextBlob(sentence)
    print("Input after parsing is {}".format(parsed))
    print("words: {}".format(parsed.words))
    print("Sentiment of the input is {}".format(parsed.sentiment))
    # pronoun, noun, adjective, verb = find_candidate_parts_of_speech(parsed)
    resp = check_for_greeting(parsed)
    return resp
    
if __name__ == '__main__':
    import sys
    if (len(sys.argv) > 1):
        print("sys.argv is {}".format(sys.argv))
        saying = sys.argv[1]
    else:
        print("Error: No input detected")
        sys.exit(1)
    print(interpret(saying))
