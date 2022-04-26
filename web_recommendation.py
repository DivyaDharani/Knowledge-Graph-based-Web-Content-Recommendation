import spacy
from collections import Counter
import traceback
import pandas as pd

#project module imports:
from clustering import get_cluster_memberships, get_dataset
from knowledge_graph import construct_knowledge_graph
import nlp_tasks as mynlp

nlp = spacy.load("en_core_web_lg")

TOP_CATEG_COUNT = 3

def recommend_web_articles(texts, user_knowledge_graph_df = None):
    recommendation_result = None
    try:
        if user_knowledge_graph_df is None:
            user_knowledge_graph_df = construct_knowledge_graph(texts)
        user_knowledge_graph_df['Combined Entities'] = user_knowledge_graph_df['Subjects and Objects'] + \
                                                       user_knowledge_graph_df['Entity List']

        entities = list(user_knowledge_graph_df['Combined Entities'])
        entities_joined = []
        for ent_list in entities:
            if len(ent_list) > 0:
                txt = mynlp.remove_stop_words(' '.join(ent_list))
                if len(txt) > 0:
                    entities_joined.append(txt)

        df = get_dataset()
        #df = pd.read_csv('final_dataset.csv')
        categories = list(df['Type'].unique())

        text_docs = [nlp(ents) for ents in entities_joined]
        category_docs = [nlp(cat) for cat in categories]

        max_score_details = []
        for doc in text_docs:
            sim_scores = []
            for i in range(len(category_docs)):
                cat_doc = category_docs[i]
                sim_scores.append((doc.similarity(cat_doc), doc.text, categories[i]))
            max_score_details.append(sorted(sim_scores, key=lambda x: x[0], reverse=True)[0])

        max_score_categories = [score[2] for score in max_score_details if score[0] > 0]
        counts = Counter(max_score_categories)
        count_tuples = list(counts.items())
        sorted_count_tuples = sorted(count_tuples, key=lambda x: x[1], reverse=True)
        categories_to_recommend = [tup[0] for tup in sorted_count_tuples[:TOP_CATEG_COUNT]]

        recom_req_dict = {}
        for categ in categories_to_recommend:
            recom_req_dict[categ] = []
        for detail in max_score_details:
            categ = detail[2]
            if categ in categories_to_recommend:
                recom_req_dict[categ].append(detail)

        # keeping only the max score detail
        for key in recom_req_dict:
            detail = recom_req_dict[key]
            recom_req_dict[key] = max(detail, key=lambda x: x[0])[1]

        #using cluster predictions from the dataset to take the recommendations
        docs = [nlp(recom_req_dict[categ]) for categ in recom_req_dict]
        vectors = [doc.vector for doc in docs]
        if len(vectors) > 0:
            cluster_memberships = get_cluster_memberships(vectors)
            print(cluster_memberships)

        recommendation_result = recom_req_dict

    except Exception as e:
        print("Error occurred in the recommend_web_articles method: ", e, traceback.print_exc())

    return recommendation_result
