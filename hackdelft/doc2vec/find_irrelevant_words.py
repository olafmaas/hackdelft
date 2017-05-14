import re
from collections import Counter


def preprocess(str):
    # remove links
    str = re.sub(r'http(s)?:\/\/\S*? ', "", str)
    return str


def preprocess_document(text):
    text = preprocess(text)
    return ''.join([x if x.isalnum() or x.isspace() else " " for x in text ]).split()

f = open("cyber-trend-index-dataset-version2.txt")
content = f.read()
f.close()

lines = content.lower().splitlines()

prep = [preprocess_document(x) for x in lines]

words = [x for sublist in prep for x in sublist]

count = Counter(words)
print(count.most_common()[:100])