import spacy
import nlp_tasks as mynlp
import pandas as pd

nlp = spacy.load("en_core_web_sm")

def construct_knowledge_graph(texts):
    sentences = []
    for text in texts:
        coref_text = mynlp.coref_resolution(text)
        doc = nlp(coref_text)
        sentences.extend([sent.text for sent in doc.sents])

    docs = [nlp(sent) for sent in sentences]

    knowledge_graph_dict_list = []
    for doc in docs:
        subjects, objects, main_subj, main_obj = mynlp.get_subjects_and_objects(doc)
        relation = mynlp.get_relation(doc)
        entities = mynlp.get_entities(doc)
        if all([not (item is None or item.strip() == '') for item in [main_subj, relation, main_obj]]):
            knowledge_graph_dict_list.append(
                {'Entity': main_subj, 'Relation': relation, 'Value': main_obj, 'Entity List': entities})

    knowledge_graph_df = pd.DataFrame(knowledge_graph_dict_list)
    return knowledge_graph_df
