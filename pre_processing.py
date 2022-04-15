from os.path import exists
import pickle
import pandas as pd
import wordninja
import spacy
from sklearn.cluster import KMeans

nlp = spacy.load("en_core_web_lg")

DATASET_PATH = 'Read_The_Web_NELL.08m.1102_dataset.csv'
CLUSTER_MODEL_PATH = 'kmeans_model.pkl'

def split_compound_word(word):
    resList = wordninja.split(word)
    word = ' '.join(resList)
    return word

def split_value(df):
    lst = []
    for index, row in df.iterrows():
        entity = split_compound_word(row['Entity'])
        value = split_compound_word(row['Value'])
        entry = [entity, value]
        lst.append(entry)
    return lst

def combine_entity_and_values(lst):
    result = []
    for row in lst:
        result.append(row[0]+' '+row[1])
    return result

def get_cluster_model(dataset_path=DATASET_PATH):

    if exists(CLUSTER_MODEL_PATH):
        cluster_model = pickle.load(open(CLUSTER_MODEL_PATH, "rb"))
        return cluster_model


    #otherwise
    #read the dataset, clean the data, create cluster model, and dump in the cluster model path

    cluster_model = create_cluster_model(dataset_path)
    return cluster_model

    #cluster_model =
    #store the cluster model
    #return cluster_model

def create_cluster_model(dataset_path = DATASET_PATH):
    file = pd.read_csv(dataset_path)
    lst = split_value(file)
    result = combine_entity_and_values(lst)

    docs = [nlp(text) for text in result]
    vectors = [doc.vector for doc in docs]
    cluster_model = KMeans(n_clusters=10, random_state=0).fit(vectors)
    pickle.dump(cluster_model, open(CLUSTER_MODEL_PATH, "wb"))
    return cluster_model

def get_cluster_memberships(X_input):
    model = get_cluster_model()
    y_pred = model.predict(X_input)
    return y_pred

if '__name__' == '__main__':
    create_cluster_model(DATASET_PATH)

