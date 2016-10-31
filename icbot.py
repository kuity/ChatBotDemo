from __future__ import print_function, unicode_literals
import random, logging, os, json, config
os.environ['NLTK_DATA'] = os.getcwd() + '/nltk_data'
from textblob import TextBlob

def preprocess_text(text):
    # 1. Convert all to lowercase for simplicity
    # 2. Ensure that there is only one 'sentence'
    return text.lower().replace(".", " ")

def is_spam(text):
    if len(text) < config.min_len:
        return True
    elif len(text) > config.max_len:
        return True
    words = text.split(' ')
    nonalpha, alpha = 0, 0
    for word in words:
        if len(word) > config.max_word_len:
            return True
        if word.isalpha():
            alpha = alpha + 1
        else:
            nonalpha = nonalpha + 1
    if alpha < config.min_alpha or nonalpha > config.max_nonalpha:
        return True

    return False

def check_for_greeting(sentence):
    for word in sentence.words:
        if word in config.GREETING_KEYWORDS:
            return True
    return False

def check_buy(sentence):
    return 'buy' in sentence

def check_rec(sentence):
    return 'recommend' in sentence

def interpret(text):
    resp = []
    sentence = preprocess_text(text)
    if is_spam(sentence):
        resp.append((config.SPAM_RESPONSE, config.texttype))
        return resp

    parsed = TextBlob(sentence)
    print("Input after parsing is {}".format(parsed))
    print("words: {}".format(parsed.words))
    print("Sentiment of the input is {}".format(parsed.sentiment))

    if check_for_greeting(parsed) is True:
        resp.append((random.choice(config.GREETING_RESPONSES), config.texttype))
    if check_buy(parsed) is True:
        resp.append(('Showing buy menu', config.buymenu))
    elif check_rec(parsed) is True:
        resp.append((random.choice(config.RECOMMENDATIONS), config.texttype))
    else:
        pol, subj = parsed.sentiment.polarity, parsed.sentiment.subjectivity
        if subj > config.subj_threshold and pol > config.pol_threshold:
            resp.append((config.GFEEDBACK_RESPONSE, config.texttype))
        elif subj > config.subj_threshold and pol < -config.pol_threshold:
            resp.append((config.BFEEDBACK_RESPONSE, config.texttype))
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
