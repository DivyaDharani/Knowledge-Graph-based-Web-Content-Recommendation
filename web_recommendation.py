import spacy
from nlp_tasks import get_entities
from collections import Counter

#project module imports:
from clustering import get_cluster_memberships

nlp = spacy.load("en_core_web_lg")

def recommend_web_articles(sents):
    docs = [nlp(sent) for sent in sents]
    entities = [get_entities(doc) for doc in docs]
    entities_joined = [' '.join(ent_list) for ent_list in entities]
    docs = [nlp(ent) for ent in entities_joined]
    vectors = [doc.vector for doc in docs]
    cluster_memberships = get_cluster_memberships(vectors)
    membership_counts = Counter(cluster_memberships)

    #To do further:
    #sort the membership counts based on the count in descending order
    #then add recommendation logic (using get_random item from cluster) - the logic should decide how many items to pick from which clusters

    #tailor recommendations based on the feedback that users give
    #get users' preferred categories and recommend based on that