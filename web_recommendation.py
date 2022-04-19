import spacy
from nlp_tasks import get_entities
from collections import Counter

#project module imports:
from clustering import get_cluster_memberships

nlp = spacy.load("en_core_web_sm")

def recommend_web_articles(user_knowledge_graph_df):
    recommendation_result = None
    try:
        entities = list(user_knowledge_graph_df['Entity List'])
        entities_joined = []
        for ent_list in entities:
            if len(ent_list) > 0:
                entities_joined.append(' '.join(ent_list))

        docs = [nlp(ent) for ent in entities_joined]
        vectors = [doc.vector for doc in docs]
        cluster_memberships = get_cluster_memberships(vectors)
        membership_counts = Counter(cluster_memberships)

        #To do further:
        #sort the membership counts based on the count in descending order
        #then add recommendation logic (using get_random item from cluster) - the logic should decide how many items to pick from which clusters

        #tailor recommendations based on the feedback that users give
        #get users' preferred categories and recommend based on that

    except Exception as e:
        print("Error occurred in the recommend_web_articles method: ", e)

    return recommendation_result