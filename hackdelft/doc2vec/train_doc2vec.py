import logging
from gensim.models.doc2vec import TaggedDocument, Doc2Vec

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class Documents(object):
    def __init__(self, documents):
        self.documents = documents

    def __iter__(self):
        for i, doc in enumerate(self.documents):
            yield TaggedDocument(words = doc, tags = [i])
file = "cyber-trend-index-dataset.txt"
corpus = open(file, "r")
lines = corpus.read().lower().split("\n")
count = len(lines)
preprocessed = []
for t in lines:
    fixed =''.join([x for x in t if x.isalnum() or x.isspace()]).split()
    preprocessed.append(fixed)

documents = Documents(preprocessed)




#iter = 1, because we keep training ourselves :)
model = Doc2Vec(size=200, dbow_words= 1, dm=0, iter=1,  window=5, seed=1337, min_count=5, workers=16,alpha=0.025, min_alpha=0.025)
model.build_vocab(documents)
for epoch in range(10):
    print("epoch "+str(epoch))
    model.train(documents, total_examples=count, epochs=1)
    model.save('cyber-trend-index-dataset.model')
    model.alpha -= 0.002  # decrease the learning rate
    model.min_alpha = model.alpha  # fix the learning rate, no decay



