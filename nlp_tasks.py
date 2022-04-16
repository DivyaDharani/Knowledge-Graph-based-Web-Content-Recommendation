import spacy
from spacy.matcher import Matcher
from spacy import displacy
import neuralcoref

nlp = spacy.load("en_core_web_lg")
neuralcoref.add_to_pipe(nlp)

def get_subjects_and_objects(doc):
    subjects = []
    objects = []
    main_subj = ""
    main_obj = ""

    prv_tok_dep = ""  # dependency tag of previous token in the sentence
    prv_tok_text = ""  # previous token in the sentence

    prefix = ""
    modifier = ""

    root_found = False
    first_obj_after_root_found = False

    for tok in doc:
        #print(f'{tok.text} - {tok.pos_} - {tok.dep_}')
        # if token is a punctuation mark then move on to the next token
        if tok.dep_ == "punct":
            continue

        # check: token is a compound word or not
        if tok.dep_ == "compound":
            prefix = tok.text
            # if the previous word was also a 'compound' then add the current word to it
            if prv_tok_dep == "compound":
                prefix = prv_tok_text + " " + tok.text

        #check: token is a modifier or not
        # if tok.dep_.endswith("mod") == True:
        #     modifier = tok.text
        #     # if the previous word was also a 'compound' then add the current word to it
        #     if prv_tok_dep == "compound":
        #         modifier = prv_tok_text + " " + tok.text

        if tok.dep_.find("subj") == True: #and ent1 == "":
            strings = filter(None, [modifier.strip(), prefix.strip(), tok.text.strip()])
            ent1 = ' '.join(strings)
            subjects.append(ent1)
            prefix = ""
            modifier = ""

        # if tok.dep_.find("obj") == True: # and ent2 == "":
        #     ent2 = (modifier + " " + prefix + " " + tok.text).strip()
        #     objects.append(ent2)
        #     prefix = ""
        #     modifier = ""

        if tok.dep_.find("obj") == True: # and ent2 == "":
            strings = filter(None, [modifier.strip(), prefix.strip(), tok.text.strip()])
            ent2 = ' '.join(strings)
            objects.append(ent2)
            prefix = ""
            modifier = ""
            if root_found and not first_obj_after_root_found:
                main_obj = ent2
                first_obj_after_root_found = True

        if tok.dep_ == "ROOT":
            if len(subjects) > 0:
                main_subj = subjects[len(subjects)-1] #taking the last subject added before the ROOT
            root_found = True

        # update variables
        prv_tok_dep = tok.dep_
        prv_tok_text = tok.text

    return (subjects, objects, main_subj, main_obj)

def get_relation(doc):
  # Matcher class object
  matcher = Matcher(nlp.vocab)

  #define the pattern
  pattern = [{'DEP':'ROOT'},
             {'DEP': 'prt', 'OP': "?"}, #added - phrasal verb checking eg.shut 'down'
            {'DEP':'prep','OP':"?"}, #eg. The company was running 'with' his money
            {'DEP':'agent','OP':"?"}, #eg. He was beaten 'by' his friends
            {'POS':'ADJ','OP':"?"}]

  #matcher.add("matching_1", None, pattern)
  matcher.add('rule1', [pattern])

  matches = matcher(doc)

  k = len(matches) - 1
  #print(matches, matches[k][1], matches[k][2], doc[matches[k][1]: matches[k][2]])

  span = doc[matches[k][1]:matches[k][2]]

  return(span.text)

def print_pos_and_dep(doc):
    for token in doc:
        print(f'{token.text} - {token.pos_} - {token.dep_}')

def get_entities(doc):
    entities = []
    #entities = [(entity.text, entity.label_) for entity in doc.ents]
    entities = [entity.text for entity in doc.ents]
    return entities

def get_similarity_score(doc1, doc2):
    return doc1.similarity(doc2)

def get_sentences(text):
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    return sentences

def get_noun_chunks(doc):
    return list(doc.noun_chunks)

def coref_resolution(text):
    """Function that executes coreference resolution on a given text"""
    doc = nlp(text)
    # fetches tokens with whitespaces from spacy document
    tok_list = list(token.text_with_ws for token in doc)
    for cluster in doc._.coref_clusters:
        # get tokens from representative cluster name
        cluster_main_words = set(cluster.main.text.split(' '))
        for coref in cluster:
            if coref != cluster.main:  # if coreference element is not the representative element of that cluster
                if coref.text != cluster.main.text and bool(set(coref.text.split(' ')).intersection(cluster_main_words)) == False:
                    # if coreference element text and representative element text are not equal and none of the coreference element words are in representative element. This was done to handle nested coreference scenarios
                    tok_list[coref.start] = cluster.main.text + \
                        doc[coref.end-1].whitespace_
                    for i in range(coref.start+1, coref.end):
                        tok_list[i] = ""

    return "".join(tok_list)

if __name__ == '__main__':

    text = "President Biden is escalating the pressure on Vladimir Putin, targeting the Russian leader, his family and his inner circle with words and actions. The Biden administration has sanctioned Putin himself, his daughters and several of his personal friends and top aides in a bid to squeeze the Russian leader over his country’s invasion of Ukraine. Biden also has stepped up his rhetoric with Putin, calling him a war criminal, saying he cannot remain in power and most recently describing his actions as genocide on Tuesday."
    #sentences = get_sentences(text)
    #for sentence in sentences:
    sentence = text
    #print('------ ', sentence)
    doc = nlp(sentence)
    subjects, objects, main_subj, main_obj = get_subjects_and_objects(doc)
    relation = get_relation(doc)


    print(subjects, objects)
    print(main_subj, '--', relation, '--', main_obj)
    print(get_entities(doc))
    print('Noun Chunks => ', get_noun_chunks(doc))


