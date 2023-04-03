import glob
import argparse
import sys
import spacy
import re
from spacy.matcher import Matcher
from spacy.tokens import Span
    
def replace_text(doc, matches, replacement):
    new_text = doc.text
    for match_id, start, end in matches:
        span = doc[start:end]
        replace_word = replacement * len(span.text)
        new_text = new_text.replace(span.text, replace_word)
    return new_text
    
def phone_encrypt(text, replacement):
    text_t = text
    #phone pattern like (xxx)-xxx-xxxx
    phone_pattern = r"[(]?\d{3}[)\s]?[-.\s]?\d{3}[-.\s]?\d{4}"
    phone_regex = re.compile(phone_pattern)
    for match in re.finditer(phone_regex, text):
        start, end = match.span()
        phone_number = match.group()
        text_t = text_t[:start] + replacement * (end - start) + text_t[end:]
    return text_t
    
def gender_encrypt(text, replacement):
    nlp = spacy.load("en_core_web_sm")
    matcher = Matcher(nlp.vocab)
    doc = nlp(text)
    gender_pattern = [{"LOWER": {"IN": ["aunt", "baby", "brother", "boyfriend", "bride", "cousin", "child", "dad", "daughter", "father", "father-in-law", "fiancé",
    "fiancée", "friend", "girlfriend", "godchild", "godfather", "godmother", "grandchild", "grandchildren", "granddaughter", "grandfather", "granddad", "grandpa", "grandparent",
    "grandparents", "grandmother", "grandma", "great-grandparents", "groom", "half-brother", "husband", "mother", "mother-in-law", "mum", "mummy", "mom", "nephew", "niece",
    "parent", "parents", "sister", "son", "stepbrother", "twin", "twin-brother", "uncle", "wife",
    "he", "his", "him", "himself", "she", "her", "hers", "herself", "I", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "they", "them", "their", "themselves"]}}]
    
    matcher.add("GENDER", [gender_pattern])
    matches = matcher(doc)
    doc = nlp(text)
    return replace_text(doc, matches, replacement)


def address_encrypt(text, replacement):
    nlp = spacy.load("en_core_web_sm")
    matcher = Matcher(nlp.vocab)
    doc = nlp(text)
    new_text = doc.text
    
    for ent in doc.ents:
        if ent.label_ == "GPE" or ent.label_ == "LOC":
            replace_word = replacement * len(ent.text)
            new_text = new_text.replace(ent.text, replace_word)
            
    return new_text


def date_encrypt(text, replacement):
    nlp = spacy.load("en_core_web_sm")
    matcher = Matcher(nlp.vocab)
    doc = nlp(text)
    new_text = doc.text
    
    for ent in doc.ents:
        if ent.label_ == "DATE" or ent.label_ == "CARDINAL":
            replace_word = replacement * len(ent.text)
            new_text = new_text.replace(ent.text, replace_word)
            
    return new_text

def name_encrypt(text, replacement):
    nlp = spacy.load("en_core_web_sm")
    matcher = Matcher(nlp.vocab)
    doc = nlp(text)
    new_text = doc.text
    
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            replace_word = replacement * len(ent.text)
            new_text = new_text.replace(ent.text, replace_word)
            
    return new_text

def encode(filename, config):
    block_character = '█'
    #block_character = 'X'
    with open(filename, 'r') as f:
        text = f.read()
        if config['names']:
            text = name_encrpty(text, block_character)
        if config['address']:
            text = address_encrpty(text, block_character)
        if config['genders']:
            text = gender_encrpty(text, block_character)
        if config['dates']:
            text = date_encrpty(text, block_character)
        if config['phones']:
            text = phone_encrypt(text, block_character)
        
        with open(config['output'] + filename + '.redacted', 'w') as out:
            out.write(text)
            print(f"new file to {config['output'] + filename + '.redacted'}.", file = config['stats'])


