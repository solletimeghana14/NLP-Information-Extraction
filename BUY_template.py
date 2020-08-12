#!/usr/bin/env python
# coding: utf-8

# In[39]:


import spacy
import neuralcoref
import sys
import json
nlp = spacy.load('en_core_web_sm')


# In[40]:


# merge_nps = nlp.create_pipe("merge_noun_chunks")
# nlp.add_pipe(merge_nps)
# merge_ents = nlp.create_pipe("merge_entities")
# nlp.add_pipe(merge_ents)


# In[41]:


neuralcoref.add_to_pipe(nlp)


# In[42]:


def filter_spans(spans):
    # Filter a sequence of spans so they don't contain overlaps
    # For spaCy 2.1.4+: this function is available as spacy.util.filter_spans()
    get_sort_key = lambda span: (span.end - span.start, -span.start)
    sorted_spans = sorted(spans, key=get_sort_key, reverse=True)
    result = []
    seen_tokens = set()
    for span in sorted_spans:
        # Check for end - 1 here because boundaries are inclusive
        if span.start not in seen_tokens and span.end - 1 not in seen_tokens:
            result.append(span)
        seen_tokens.update(range(span.start, span.end))
    result = sorted(result, key=lambda span: span.start)
    return result


# In[43]:


def get_final_object(obj, r_subtree):
    if obj.n_rights:
        r_subtree += list(obj.rights)
        for child in obj.rights:
            get_final_object(child, r_subtree)
    return r_subtree


# In[44]:


def get_final_subject(sub, l_subtree):
    if sub.n_lefts:
        l_subtree += list(sub.lefts)
        for child in sub.lefts:
            get_final_subject(child, l_subtree)
    return l_subtree


# In[45]:


def get_source(token):
    source = None
    for child in token.rights:
        if child.text == 'of' or child.text == 'in':
            if child.right_edge.ent_type_ != 'GPE' and child.right_edge.pos_ in ('PROPN','NOUN'):
                source = child.right_edge
        if child.text == 'from':
            source = child.right_edge
    return source


# In[46]:


def resolve_coref(token):
    try:
        if token._.in_coref:
            token = token._.coref_clusters[0][0]
    finally:
        return token


# In[47]:


def show_buy_relations(doc, file_name): 
    #doc = doc._.coref_resolved
    print('Processing template....')
    sents = list(doc.sents)
    buy_relations = []
    #relation_dict = {"template": "BUY", "sentences": [], "arguments": {"1": "", "2": "", "3": "","4": "","5": ""}
    json_template = {"document": file_name, "extraction":[]}
    for sent in sents:
        try:
            spans = list(sent.ents) + list(sent.noun_chunks)
            spans = filter_spans(spans)
            with doc.retokenize() as retokenizer:
                for span in spans:
                    retokenizer.merge(span)
            final_subject = None
            final_object = ''
            source = ''
            amount = ''
            buy_match = False
            relation = ''
            main_subject = None
            quantity = ''
            relation_dict = {"template": "BUY", "sentences": [], "arguments": {"1": "", "2": "", "3": "","4": "","5": ""}}
            for token in sent:
                if token.ent_type_ == "MONEY":
                    amount = token.text
                    i = 1
                    while token.nbor(-i).pos_ in ('SYM','NUM'):
                        amount = token.nbor(-i).text + ' ' + amount
                        i += 1
                if token.dep_ == "nsubj" and main_subject is None:
                    main_subject = token
                if token.lemma_ == 'buy' or token.lemma_ == 'acquire' or token.lemma_ == 'purchase':
                    buy_match = True
                    relation = token
                    subject = [w for w in token.lefts if w.dep_ == "nsubj"]
                    obj = [w for w in token.rights if w.dep_ == "dobj"]
                    if subject:
                        final_subject = subject[0]
                    if obj:
                        final_object = obj[0]
                        r_subtree = get_final_object(obj[0], [])
                        source = get_source(token)
                        for child in r_subtree:
                            #print(r_subtree,child,child.ent_type_)
                            if child.text == 'of'  or child.text == 'from' or child.text == 'in' :
                                if child.ent_type_ != 'GPE' and source is None:
                                    source = child.right_edge
                            if child.ent_type_ == "MONEY":
                                amount = child  
                            if child.ent_type_ == "QUANTITY":
                                quantity = child  
                        if final_object.n_rights:
    #                         edge.pos_ == 'PROPN':
    #                         final_object = final_object.right_edge   
                            right_PN = [w for w in final_object.rights if w.pos_ == "PROPN"]
                            if right_PN:
                                final_object = right_PN[0]
                    if not subject and not obj:
                        obj = [w for w in token.lefts if w.dep_ == "nsubjpass"]
                        subject = [w for w in token.subtree if w.dep_ == "pobj" and w.nbor(-1).text == 'by']
                        final_object = obj[0] if obj else ''
                        final_subject = subject[0] if subject else None   
                    if final_subject is None:
                        l_subtree = get_final_subject(token.head, [])
                        #print(l_subtree)
                        final_subject = [w for w in l_subtree if w.dep_ == 'nsubj']
                        final_subject = final_subject[0] if final_subject else main_subject
                #if token.ent_type
            if buy_match:
    #             if final_subject and final_subject.pos_ == 'PRON':
    #                 print(final_subject)
    #                 try:
    #                     if final_subject._.in_coref:
    #                         print(final_subject._.coref_clusters)
    #                         final_subject = final_subject._.coref_clusters[0][0]
    #                         print(final_subject) 
    #                 except:
    #                     print('exception')
    #             else:
    #                 print('no subject')
                buy_relations.append({(final_subject, relation, final_object, source, amount) : sent})
                relation_dict["sentences"].append(sent.text)
                relation_dict["arguments"]["1"] = final_subject.text if final_subject else ""
                relation_dict["arguments"]["2"] = final_object.text if final_object else ""
                relation_dict["arguments"]["3"] = amount if amount else ""
                relation_dict["arguments"]["4"] = quantity.text if quantity else ""
                relation_dict["arguments"]["5"] = source.text if source else ""
                json_template["extraction"].append(relation_dict)
        except:
            continue
                #displacy.render(sent, style='dep', jupyter=True)
                #print(buy_relations[-1])
    #print(json_template)
    #return buy_relations
    print('Template processed.')
    return json_template
            


# In[48]:


def create_nlpdoc_object(file_name):
    #relations = None
    with open(file_name, 'r', encoding='utf-8',errors="ignore") as file:
        content = file.read()
        doc = nlp(content)
        #relations = show_buy_relations(doc)
    return doc


# In[49]:

#with os.scandir('WikipediaArticles/') as directory:
#    for entry in directory:
        #print(entry.name)
file_name = sys.argv[1]

try:    
    coref = sys.argv[2]
except IndexError:
    coref = ''
    
doc = create_nlpdoc_object(file_name)
if(coref == 'c'):
    #neuralcoref.add_to_pipe(nlp)
    doc = nlp(doc._.coref_resolved)
    print('processing with coref resolution...')
json_buy = show_buy_relations(doc, file_name)

json_file = file_name[:len(file_name)-4] + ".json"
json_object = json.loads(json.dumps(json_buy))
json_formatted_str = json.dumps(json_object, indent=4)
file = open(json_file, "a+")
n = file.write(json_formatted_str)
file.close()
print('saved to JSON')


# In[ ]:





# In[ ]:





# In[ ]:




