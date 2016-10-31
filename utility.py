def find_pronoun(sent):
    pronoun = None
    for word, part_of_speech in sent.pos_tags:
        pronoun = word
    return pronoun

def find_verb(sent):
    verb = None
    pos = None
    for word, part_of_speech in sent.pos_tags:
        if part_of_speech.startswith('VB'):
            verb = word
            pos = part_of_speech
            break
    return verb, pos

def find_noun(sent):
    noun = None
    for word, part_of_speech in sent.pos_tags:
        if part_of_speech == 'NN':  # This is a noun
            noun = word
            break
    return noun

def find_adjective(sent):
    """Given a sentence, find the best candidate adjective."""
    adj = None
    for word, part_of_speech in sent.pos_tags:
        if part_of_speech == 'JJ':  # This is an adjective
            adj = word
            break
    return adj

def find_candidate_parts_of_speech(sentence):
    pronoun = find_pronoun(sentence)
    noun = find_noun(sentence)
    adjective = find_adjective(sentence)
    verb = find_verb(sentence)
    logger.info("Pronoun=%s, noun=%s, adjective=%s, verb=%s", pronoun, noun, adjective, verb)
    return pronoun, noun, adjective, verb