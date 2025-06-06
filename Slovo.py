import pymorphy3

morph = pymorphy3.MorphAnalyzer()

def normalize_word(word):
    p = morph.parse(word)[0]
    return p.normal_form


def slovo(word):
 normalized_word = normalize_word(word)
 return normalized_word 

