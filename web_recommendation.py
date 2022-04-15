import spacy
import pre_processing
from nlp_tasks import get_entities

nlp = spacy.load("en_core_web_lg")

def recommend_web_articles(sents):
    docs = [nlp(sent) for sent in sents]
    entities = [get_entities(doc) for doc in docs]
    entities_joined = [' '.join(ent_list) for ent_list in entities]
    docs = [nlp(ent) for ent in entities_joined]
    vectors = [doc.vector for doc in docs]
    cluster_memberships = pre_processing.get_cluster_memberships(vectors)




#To do:
#Change pre_processing file name
#Include cache for cluster model in get_cluster_model method