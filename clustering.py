from os.path import exists
import pickle
import pandas as pd
import spacy
from sklearn.cluster import KMeans

nlp = spacy.load("en_core_web_lg")

DATASET_PATH = 'final_dataset.csv'
CLUSTER_MODEL_PATH = '_kmeans_model.pkl'
NUM_CLUSTERS = 400
DEFAULT_CATEGORY = 'All'

saved_cluster_model_dict = {}
saved_dataset = None

def combine_entity_and_categories(df, category):
    '''lst = df[['Entity', 'Type']].values().tolist()

    for row in lst:
        result.append(' '.join(row))'''
    result = []
    if category == DEFAULT_CATEGORY:
        result = df['Entity'].to_list()
    else:
        result_df = df[df['Type'] == category]
    return result

def get_cluster_model(dataset_path=DATASET_PATH, cluster_model_dict=saved_cluster_model_dict, category=DEFAULT_CATEGORY):
    global saved_cluster_model_dict
    if category in cluster_model_dict:
        return cluster_model_dict[category]
    category_cluster_path = category + CLUSTER_MODEL_PATH
    if exists(category_cluster_path):
        saved_cluster_model_dict[category] = pickle.load(open(CLUSTER_MODEL_PATH, "rb"))
        return saved_cluster_model_dict[category]

    saved_cluster_model_dict[category] = create_cluster_model(dataset_path, category)
    return saved_cluster_model_dict[category]

def get_dataset(dataset_path=DATASET_PATH, dataset=saved_dataset):
    if dataset is not None:
        return dataset
    global saved_dataset
    saved_dataset = pd.read_csv(dataset_path)
    return saved_dataset

def create_cluster_model(dataset_path=DATASET_PATH, category=DEFAULT_CATEGORY):
    df = get_dataset(dataset_path)
    result = combine_entity_and_categories(df, category)
    docs = [nlp(text) for text in result]
    vectors = [doc.vector for doc in docs]
    cluster_model = KMeans(n_clusters=NUM_CLUSTERS, random_state=0).fit(vectors)
    category_cluster_path = category + CLUSTER_MODEL_PATH
    pickle.dump(cluster_model, open(category_cluster_path, "wb"))
    return cluster_model

def get_cluster_memberships(X_input, category):
    model = get_cluster_model(category=category)
    y_pred = model.predict(X_input)
    return y_pred

def get_cluster_elements(cluster_id):
    model = get_cluster_model()
    dataset = get_dataset()
    cluster_map = pd.DataFrame()
    cluster_map['data_index'] = dataset.index.values
    cluster_map['cluster'] = model.labels_
    cluster_elements = cluster_map[cluster_map.cluster == cluster_id]
    result = dataset.loc[cluster_elements.data_index, :]
    return result

def get_random_item_from_cluster(cluster_id):
    cluster_elements = get_cluster_elements(cluster_id)
    return cluster_elements.sample()


if __name__ == '__main__':
    create_cluster_model(DATASET_PATH, DEFAULT_CATEGORY)


#To do:
#get_random_item_from_cluster should return 'entity value' as string
#decide how many clusters should be formed based on analysing the dataset manually (and based on how the recommendations come out to be)
