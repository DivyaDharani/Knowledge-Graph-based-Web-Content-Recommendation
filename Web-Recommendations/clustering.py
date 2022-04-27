from os.path import exists
import pickle
import pandas as pd
import spacy
from sklearn.cluster import KMeans

nlp = spacy.load("en_core_web_lg")

DATASET_PATH = 'final_dataset.csv'
CLUSTER_MODEL_PATH = '_kmeans_model.pkl'
MIN_NUM_CLUSTERS = 50
DEFAULT_CATEGORY = 'All'

saved_cluster_model_dict = {}
saved_dataset = None

def get_dataset(dataset_path=DATASET_PATH, dataset=saved_dataset):
    if dataset is not None:
        return dataset
    global saved_dataset
    saved_dataset = pd.read_csv(dataset_path)
    return saved_dataset

def get_category_dataset(category, dataset_path=DATASET_PATH):
    df = get_dataset(dataset_path)
    if category == DEFAULT_CATEGORY:
        return df
    else:
        result_df = df[df['Type'] == category]
        return result_df

def get_cluster_model(category=DEFAULT_CATEGORY):
    global saved_cluster_model_dict
    if category in saved_cluster_model_dict:
        return saved_cluster_model_dict[category]
    category_cluster_path = category + CLUSTER_MODEL_PATH
    if exists(category_cluster_path):
        saved_cluster_model_dict[category] = pickle.load(open(category_cluster_path, "rb"))
        return saved_cluster_model_dict[category]

    saved_cluster_model_dict[category] = create_cluster_model(category)
    return saved_cluster_model_dict[category]

def create_cluster_model(category=DEFAULT_CATEGORY):
    category_dataset = get_category_dataset(category=category)
    result = category_dataset['Entity'].to_list()
    docs = [nlp(text) for text in result]
    vectors = [doc.vector for doc in docs]
    no_clusters = min(MIN_NUM_CLUSTERS, len(result))
    cluster_model = KMeans(n_clusters=no_clusters, random_state=0).fit(vectors)
    category_cluster_path = category + CLUSTER_MODEL_PATH
    pickle.dump(cluster_model, open(category_cluster_path, "wb"))
    return cluster_model

def get_cluster_memberships(X_input, category):
    model = get_cluster_model(category=category)
    y_pred = model.predict(X_input)
    return y_pred

def get_cluster_elements(cluster_id, category):
    model = get_cluster_model(category=category)
    dataset = get_category_dataset(category=category)
    cluster_map = pd.DataFrame()
    cluster_map['data_index'] = dataset.index.values
    cluster_map['cluster'] = model.labels_
    cluster_elements = cluster_map[cluster_map.cluster == cluster_id]
    result = dataset.loc[cluster_elements.data_index, :]
    return result

def get_random_item_from_cluster(cluster_id, category, number_of_samples=3):
    cluster_elements = get_cluster_elements(cluster_id, category)
    cluster_elements_entity = cluster_elements['Entity']
    min_number_samples = min(number_of_samples, len(cluster_elements_entity.index))
    sample = cluster_elements_entity.sample(min_number_samples)
    return sample.to_list()


if __name__ == '__main__':
    create_cluster_model(DEFAULT_CATEGORY)


#To do:
#get_random_item_from_cluster should return 'entity value' as string
#decide how many clusters should be formed based on analysing the dataset manually (and based on how the recommendations come out to be)
