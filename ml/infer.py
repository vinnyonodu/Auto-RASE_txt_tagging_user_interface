from flair.models import SequenceTagger
from flair.data import Sentence
import os
import pathlib
import sys
import re

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

def infer(text):
    # Load the trained model
    cwd = os.getcwd()
    path = f'{cwd}\ml\models\\best-model.pt'
    print(path)
    model = SequenceTagger.load(path)

    text_split = text.split(".")

    final_string = ""
    a = []
    for x in text_split:
        sentence = Sentence(x)
        model.predict(sentence)
        value = sentence.to_tagged_string()
        a.append(value)
        value_split = value.split('\u2192')[-1]



        pattern = r'"([^"]*)"/\w+'
        extracted_items = re.findall(pattern, value_split)

        pattern_2 = r'"/([A-Z][a-z]*)'
        extracted_items_tags =  re.findall(pattern_2, value_split)


        for i, item in enumerate(extracted_items):
            final_string += f"<strong>{extracted_items_tags[i]}</strong>: {item}<br>"


    return final_string

