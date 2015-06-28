## This script is super slow. Converting every string into a TextBlob object is really expensive.

from __future__ import print_function

###!!! Fixing error 'ascii' codec can't decode byte...
import sys
reload(sys)
sys.setdefaultencoding('Cp1252')
###!!! End fixing codec

###!!! Setting directory for questions
dir_data_questions = "data/c040_questions/"
###!!!

def clean_string(text):
    ''' Takes a string, lowercase, tokenizes, lematizes, and removes stopwords, and returns a single string again '''
    from nltk import stem
    from nltk.tokenize import RegexpTokenizer
    from nltk.corpus import stopwords
    import unicodedata
    tokenizer = RegexpTokenizer(r'\b\w\w+\b')
    #stemmer = stem.snowball.EnglishStemmer()
    lemmer = stem.WordNetLemmatizer()
    #stopper = stopwords.words('english')
#     if type(text) == unicode:
#         text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
    words = text.lower()
    words = tokenizer.tokenize(words)
    for word in words:
        if type(word) == unicode:
            print(word)
            word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore')
    #words = [lemmer.lemmatize(w) for w in words]    
    #words = [i for i in words if i not in stopper]
    return ' '.join(words)
 

def read_q(filename):
    d = []
    q = []
    with open(filename, 'r') as f:
        for line in f:
            ls = line.split(' +++$+++ ')
            d.append(ls[0])
            #print(ls[0])
            q.append(clean_string(ls[1]))
    return q, d
    






## get the feature table 
feature_table_file = 'data/c030_transcripts/feature_table.txt'
import pandas as pd
feature_table = pd.read_csv(feature_table_file, sep='\t', index_col=0)    
 


X = []
q_dir = dir_data_questions
import os
for file in os.listdir(q_dir):
    thisJ_qlist, docks = read_q(q_dir + file)
    X.append( thisJ_qlist )
    dockets = docks

from textblob import TextBlob
S = {}
for i in range(len(dockets)):
    docket = dockets[i]
    ## Petitioner is file 0; Respondent is file 1.  Res - Pet > 0 favors Respondent
    ## files 0,2,4,6,8 should be petitioners, 1,3,5,7,9 should be respondents
    S[docket] = {'sentiment_BREYER':0.0, 'sentiment_GINSBURG':0.0, 'sentiment_KENNEDY':0.0, 'sentiment_ROBERTS':0.0, 'sentiment_SCALIA':0.0}
    S[docket]['sentiment_BREYER'] = TextBlob(X[0][i]).sentiment[0] - TextBlob(X[1][i]).sentiment[0]
    S[docket]['sentiment_GINSBURG'] = TextBlob(X[2][i]).sentiment[0] - TextBlob(X[3][i]).sentiment[0]
    S[docket]['sentiment_KENNEDY'] = TextBlob(X[4][i]).sentiment[0] - TextBlob(X[5][i]).sentiment[0]
    S[docket]['sentiment_ROBERTS'] = TextBlob(X[6][i]).sentiment[0] - TextBlob(X[7][i]).sentiment[0]
    S[docket]['sentiment_SCALIA'] = TextBlob(X[8][i]).sentiment[0] - TextBlob(X[9][i]).sentiment[0]
     

## Convert to a DataFrame, sort columns by name, and inner join with feature_table
Sd = pd.DataFrame.from_dict(S, orient='index')
Sd.sort(axis=1, inplace=True)
feature_table = feature_table.join(Sd,how='inner')


outfile = 'data/c050_sentiment/feature_table_2.txt'
feature_table.to_csv(outfile, sep='\t')

