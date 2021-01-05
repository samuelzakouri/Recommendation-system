import pandas as pd 
import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.compose import ColumnTransformer
import os 
import time
import pickle


PATH = "/Users/samuel/Documents/Projets/Reco_movies/"

def load_main_data():
    
    """
    Returns
    -------
    df : DataFrame
        Main dataframe used to calculate the cosine similarity.

    """
    df = pd.read_csv(PATH + 'Data/imdb_cleaned_data.csv', index_col=0, decimal=',', dtype={'RELEASE_YEAR':'O'})

    
    return df

def process_data(df):
    
   """
    Converting strings to lowercase and then encode the four variables that we use and returns the transformed variables.

    Parameters
    ----------
    df : DataFrame
        Original dataframe.
   
    Returns
    -------
    X_trans : Array
        Encoded variables.

    """
    
   # Converting strings to lowercase.
   for col in df.columns.difference(['ORIGINAL_TITLE']):
       try:
           df[col] = df[col].str.lower()
       except:
           pass
       
   #the four variables that we use to calculate the similarity between movies
   X = df[['CAST','DIRECTOR','OVERVIEW','GENRES','PRODUCTION_COMPANIES']]
   
   #Stopwords
   SW = set(ENGLISH_STOP_WORDS)
   
   
   #The count vectorizer is different for each variable
   ct = ColumnTransformer(transformers=
    [('cast_countvectorizer', CountVectorizer(ngram_range=(2,2)),'CAST'),
     ('director_countvectorizer', CountVectorizer(ngram_range=(2,2)), 'DIRECTOR'),
     ('overview_countvectorizer', CountVectorizer(stop_words=SW),'OVERVIEW'),
     ('genres_countvectorizer', CountVectorizer(),'GENRES'),
     ('production_countvectorizer', CountVectorizer(ngram_range=(1,3)),'PRODUCTION_COMPANIES')
     ],
    remainder='passthrough')
   
   X_trans = ct.fit_transform(X)
   
   return X_trans
   

def cos_similarity(X):
    """
    Calculate the cosine similarity between movies

    Parameters
    ----------
    X : Array
        Encoded variables.

    Returns
    -------
    cosine_sim : Array
        The cosine similarity matrix.

    """
    
    cosine_sim = cosine_similarity(X)
    
    return cosine_sim 


#######################################################################################

start = time.time()

df = load_main_data()

X_trans = process_data(df)

cosine_sim = cos_similarity(X_trans)

PATH_SIM = PATH + 'Similarity/'

if not os.path.exists(PATH_SIM):
        os.makedirs(PATH_SIM)

df_similarity = pd.DataFrame(df['ORIGINAL_TITLE'])
df_similarity['FORMATED_ORIGINAL_TITLE'] = df['ORIGINAL_TITLE'].str.lower()
df_similarity = df_similarity.merge(pd.DataFrame(cosine_sim), right_index=True,left_index=True)

with open(PATH_SIM + 'similarity.pkl', 'wb') as f:
        pickle.dump(df_similarity, f)
   
   
   
print('Similarity dataframe generation took', np.round(time.time() - start), 'seconds')   