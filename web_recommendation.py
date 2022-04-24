import spacy
from collections import Counter
import traceback
from mining import extract_text

#project module imports:
from clustering import get_cluster_memberships
from knowledge_graph import construct_knowledge_graph

nlp = spacy.load("en_core_web_sm")

def recommend_web_articles(texts, user_knowledge_graph_df = None):
    recommendation_result = None
    try:
        if user_knowledge_graph_df is None:
            user_knowledge_graph_df = construct_knowledge_graph(texts)

        print(user_knowledge_graph_df, user_knowledge_graph_df['Entity List'])

        entities = list(user_knowledge_graph_df['Entity List'])
        entities_joined = []
        for ent_list in entities:
            if len(ent_list) > 0:
                entities_joined.append(' '.join(ent_list))
        docs = [nlp(ent) for ent in entities_joined]
        vectors = [doc.vector for doc in docs]
        if len(vectors) > 0:
            cluster_memberships = get_cluster_memberships(vectors)
            membership_counts = Counter(cluster_memberships)

        #To do further:
        #sort the membership counts based on the count in descending order
        #then add recommendation logic (using get_random item from cluster) - the logic should decide how many items to pick from which clusters

        #tailor recommendations based on the feedback that users give
        #get users' preferred categories and recommend based on that
            return membership_counts, cluster_memberships

    except Exception as e:
        print("Error occurred in the recommend_web_articles method: ", e, traceback.print_exc())
    recommendation_result = ["recommendation_link1", "recommendation_link2", "recommendation_link3"]

    return recommendation_result


sample_texts = ["An earthquake is the ground shaking caused by a sudden slip on a fault.",
"The stock market broadly refers to the collection of exchanges and other venues where the buying, selling, and issuance of shares of publicly held companies take place. ",
"A mutual fund is a company that pools money from many investors and invests the money in securities such as stocks, bonds, and short-term debt.",
"Warren Edward Buffett is an American business magnate, investor, and philanthropist."]


def get_recommendations(links):
    texts = extract_text(links)
    print(texts)
    #texts = []
    recommended_links = recommend_web_articles(texts)
    #recommended_links = ["recommendation_link1", "recommendation_link2", "recommendation_link3"]
    return recommended_links
