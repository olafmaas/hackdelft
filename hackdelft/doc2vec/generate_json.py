import json
import re

import nltk
from gensim.models import Doc2Vec
from nltk.cluster import KMeansClusterer
from nltk.corpus import stopwords

NUM_CLUSTERS = 15

def preprocess(str):
    # remove links
    str = re.sub(r'http(s)?:\/\/\S*? ', "", str)
    return str


def preprocess_document(text):
    text = preprocess(text)
    return ''.join([x if x.isalnum() or x.isspace() else " " for x in text ]).split()



with open('dataset-links.txt') as data_file:
    data = json.load(data_file)

fname = "cyber-trend-index-dataset.model"
model = Doc2Vec.load(fname)

duplicate_abstracts = {}

used_objects = []
vectors = []
for i, d in enumerate(data):
    abstract = d["abstract"].lower()
    if abstract not in duplicate_abstracts:
        duplicate_abstracts[abstract] = True
        used_objects.append(d)
        vectors.append(model.infer_vector(preprocess_document(abstract)))

kclusterer = KMeansClusterer(NUM_CLUSTERS, distance=nltk.cluster.util.cosine_distance, repeats=25)
assigned_clusters = kclusterer.cluster(vectors, assign_clusters=True)

def get_objects_by_cluster(id):
    list = []
    for x in range(0, len(assigned_clusters)):
        if (assigned_clusters[x] == id):
            list.append(used_objects[x])
    return list

def get_topics(objects):
    from collections import Counter
    words = [preprocess_document(x["abstract"].lower()) for x in objects]
    words = [word for sublist in words for word in sublist]
    filtered_words = [word for word in words if word not in stopwords.words('english') and not word.isdigit()]
    count = Counter(filtered_words)
    return count.most_common()[:5]

json_data = []
for i in range(0,NUM_CLUSTERS):
    cur_obj = {}
    objects = get_objects_by_cluster(i)
    topics = get_topics(objects)
    avgactivity = 0
    goodactivity = 0
    goodcount = 0
    for x in range(0, len(objects)):
        avgactivity+=int(objects[x].get("activity"))/len(objects)
        goodactivity += int(objects[x].get("activity"))
        if (int(objects[x].get("activity")) > 0): goodcount+=1
    goodactivity=goodactivity/goodcount
    cur_obj["topics"] = topics
    cur_obj["avgactivity"] = avgactivity
    cur_obj["goodactivity"] = goodactivity
    cur_obj["articles"] = objects
    json_data.append(cur_obj)

f = open("output.json", "w")
json.dump(json_data, f)
f.close()