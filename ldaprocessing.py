import numpy as np
import pandas as pd
import re

# Plotly imports
import plotly.offline as py
import plotly.graph_objs as go
import plotly.tools as tls

# Other imports
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from matplotlib import pyplot as plt
## %matplotlib inline
import nltk
from nltk.stem import WordNetLemmatizer
lemm = WordNetLemmatizer()

class LemmaCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        analyzer = super(LemmaCountVectorizer, self).build_analyzer()
        return lambda doc: (lemm.lemmatize(w) for w in analyzer(doc))
    
    
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    return text

def print_top_words(model, feature_names, n_top_words):
    for index, topic in enumerate(model.components_):
        message = "\nTopic #{}:".format(index + 1)
        message += " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1 :-1]])
        print(message)
        print("="*90)
        
train = #insert dataframe

#stopwords = nltk.corpus.stopwords.words('english')
#for headline in train["headline"]:
#    headline_list = nltk.word_tokenize(headline)
#    headline_list_clean = [word for word in headline_list if word.lower() not in stopwords]
    
text = list(train["Headline"].values)
# Calling our overwritten Count vectorizer
tf_vectorizer = LemmaCountVectorizer(max_df=0.95, min_df=2, preprocessor=preprocess_text, stop_words='english', decode_error='ignore')
tf = tf_vectorizer.fit_transform(text)

#feel free to edit the number of components (topic) and other parameters
lda = LatentDirichletAllocation(n_components=3, max_iter=300, learning_method = 'online', learning_offset = 50., random_state = 0)
lda.fit(tf)
tf_feature_names = tf_vectorizer.get_feature_names()
print_top_words(lda, tf_feature_names, 10)
