from __future__ import print_function, unicode_literals
import random, logging, os, json, config
os.environ['NLTK_DATA'] = './nltk_data/'
from textblob import TextBlob

class Logic:
    def __init__(self, cond, keyword, ncond, optype, resp):
        self.condition = cond
        self.ncondition = ncond
        self.keyword = keyword
        self.optype = optype            
        self.response = resp
    def prn(self):
        print ('Condition: {}, Keyword: {}, New Condition: {}, Response Type: {},  Response: {}'.format(
                    self.condition,
                    self.keyword,
                    self.ncondition,
                    self.optype,
                    self.response))

def parseConfig():
    inp = config.input
    parsedConfig = []
    with open(inp, 'r') as f:
        for line in f:
            tokens = line.strip().split(config.conf_delimiter)
            optype = tokens[3]
            if optype == config.menu:
                title = tokens[4]
                mlen = len(tokens)
                moptions = []
                for index in range(5, mlen):
                    print(index)
                    moptions.append(tokens[index].split(config.menu_delimiter))
                resp = (title, moptions)
                parsedConfig.append(Logic(tokens[1], tokens[0], tokens[2], tokens[3], resp))
            else:
                parsedConfig.append(Logic(tokens[1], tokens[0], tokens[2], tokens[3], tokens[4]))

    for c in parsedConfig:
        c.prn()
    return parsedConfig

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
    if nonalpha > config.max_nonalpha:
        return True
    return False

def interpret(text, conf, state):
    resp = []
    sentence = preprocess_text(text)
    #if is_spam(sentence):
    #    return (config.texttype, config.default_response, config.default_state)

    parsed = TextBlob(sentence)
    print("Current state is {}".format(state))
    print("Input after parsing is {}".format(parsed))
    print("words: {}".format(parsed.words))
    print("Sentiment of the input is {}".format(parsed.sentiment))

    for l in conf:
        if state != l.condition:
            continue
        if l.keyword in parsed.words:
            return (l.optype, l.response, l.ncondition)

    return (config.texttype, config.default_response, config.default_state)

if __name__ == '__main__':
    import sys
    c = parseConfig()
    if (len(sys.argv) > 1):
        print("sys.argv is {}".format(sys.argv))
        saying = sys.argv[1]
    else:
        print("Error: No input detected")
        sys.exit(1)
    print(interpret(saying, c, 'null'))
