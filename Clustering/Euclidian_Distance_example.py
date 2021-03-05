from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import euclidean_distances

corpus = [
'All my cats in a row',
'When my cat sits down, she looks like a Furby toy!',
'The cat from outer space',
'Sunshine loves to sit like this for some reason.'
]

vectorizer = CountVectorizer()
features = vectorizer.fit_transform(corpus).todense() 
print( vectorizer.vocabulary_ )

for f in features:
    print( euclidean_distances(features[0], f) )
