import nltk
from gensim.models import Doc2Vec
from nltk.cluster.kmeans import KMeansClusterer
NUM_CLUSTERS = 10

def preprocess_document(text):
    return ''.join([x if x.isalnum() or x.isspace() else " " for x in text ]).split()

#data = <sparse matrix that you would normally give to scikit>.toarray()
fname = "cyber-trend-index-dataset.model"
model = Doc2Vec.load(fname)

file = "dataset.txt"
corpus = open(file, "r")
lines = corpus.read().lower().split("\n")[0:1000]
count = len(lines)

vectors = []

print("inferring vectors")
for t in lines:
    vectors.append(model.infer_vector(preprocess_document(t)))
print("done")



kclusterer = KMeansClusterer(NUM_CLUSTERS, distance=nltk.cluster.util.cosine_distance, repeats=25)
assigned_clusters = kclusterer.cluster(vectors, assign_clusters=True)
#print(assigned_clusters)
means = kclusterer.means()
print(means)
for mean in means:
    print(model.most_similar(positive=[mean], topn=10))
    print("\n")
