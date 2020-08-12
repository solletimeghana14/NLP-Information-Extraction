#!/usr/bin/env python
# coding: utf-8

# In[135]:


import spacy
import neuralcoref
import sys
import json
nlp = spacy.load('en_core_web_sm')

# In[136]:


neuralcoref.add_to_pipe(nlp)


# In[137]:


job_list = ['actress',
 'host',
 'producer',
 'philanthropist',
 'queen',
 'barber',
 'president',
 'miner',
 'city councilman',
 'farmer',
 'preacher',
 'maid',
 'student',
 'news anchor',
 'critic',
 'columnist',
 'candidate',
 'author',
 'housewife',
 'judge',
 'princess',
 'personal trainer',
 'reader',
 'model student',
 'journalist',
 'biographer',
 'reporter',
 'king',
 'filmmaker',
 'editor',
 'therapist',
 'entertainer',
 'ceo',
 'senator',
 'chairman',
 'politician',
 'leader',
 'pope',
 'springer',
 'professor',
 'attorney',
 'governor',
 'crown prince',
 'teacher',
 'premier',
 'mayor',
 'magician',
 'executive producer',
 'magnate',
 'vice president',
 'founder',
 'congressman',
 'stockbroker',
 'salesman',
 'analyst',
 'general',
 'janitor',
 'boss',
 'doctor',
 'activist',
 'owner',
 'director',
 'trader',
 'chief financial officer',
 'publisher',
 'companion',
 'assistant coach',
 'manager',
 'mediator',
 'secretary of the treasury',
 'actuary',
 'manufacturer',
 'river',
 'surveyor',
 'lieutenant governor',
 'commander',
 'envoy',
 'lieutenant colonel',
 'translator',
 'captain',
 'colonel',
 'commander colonel',
 'brigadier general',
 'major general',
 'guard',
 'soldier',
 'secretary',
 'baron',
 'chief of staff',
 'major',
 'admiral',
 'president general',
 'coach',
 'chancellor',
 'administrator',
 'merchant',
 'attorney general',
 'secretary of state',
 'secretary of war',
 'diplomat',
 'chief justice',
 'negotiator',
 'minister',
 'principal',
 'secretary of treasury',
 'historian',
 'lieutenant general',
 'speaker',
 'reverend',
 'architect',
 'dentist',
 'dancer',
 'pastor',
 'creator',
 'charter',
 'entrepreneur',
 'engineer',
 'designer',
 'co-founder',
 'co-chairman',
 'model',
 'pilot',
 'sailor',
 'commodore',
 'guide',
 'chief executive officer',
 'chief technology officer',
 'astronaut',
 'scientist',
 'gen.',
 'geographer',
 'emperor',
 'theologian',
 'printer manufacturer',
 'recorder',
 'general manager',
 'salesmen',
 'vendor',
 'graphic designer',
 'inventor',
 'secretary of housing and urban development',
 'secretary of transportation',
 'referee',
 'dealer',
 'driver',
 'collector',
 'vice-president',
 'demonstrator',
 'cell maker',
 'private',
 'spokesman',
 'buyer',
 'cfo',
 'managing director',
 'chief executive',
 'retailer',
 'printer',
 'developer',
 'processor',
 'grip',
 'chief operating officer',
 'assistant',
 'layer',
 'operator',
 'header',
 'writer',
 'singer',
 'evangelist',
 'executive director',
 'general counsel',
 'city manager',
 'physician',
 'importer',
 'explorer',
 'empress',
 'boxer',
 'general secretary',
 'party leader',
 'representative',
 'secretary of defense',
 'prince',
 'director-general',
 'fund manager',
 'surgeon',
 'cook',
 'comptroller',
 'refiner',
 'tanker',
 'vice-chairman',
 'executive chairman',
 'constable',
 'interim president',
 'nobel laureate',
 'dean',
 'artist',
 'landscape architect',
 'consultant',
 'chef',
 'vice chairman',
 'superior',
 'jeweler',
 'specialist',
 'broker',
 'strategist',
 'treasury secretary',
 'underwriter',
 'quality control supervisor',
 'auditor',
 'spokeswoman',
 'district attorney',
 'principal author',
 'treasurer',
 'lobbyist',
 'deputy mayor',
 'communications director',
 'assistant attorney general',
 'executive vice president',
 'chief compliance officer',
 'lawyer',
 'spokesperson',
 'technician',
 'intelligence director',
 'hacker',
 'astronomer',
 'composer',
 'aerospace engineer',
 'homemaker',
 'marketing manager',
 'businesswoman',
 'monk',
 'explorer captain',
 'builder',
 'state treasurer',
 'superintendent',
 'governor general',
 'prime minister',
 'chief minister',
 'poet',
 'novelist',
 'indian activist',
 'clerk',
 'barrister',
 'priest',
 'landlady',
 'magistrate',
 'police officer',
 'saint',
 'dictator',
 'representative leader',
 'governor-general',
 'marshal',
 'philosopher',
 'butcher',
 'missionary',
 'sultan',
 'interpreter',
 'economist',
 'physicist',
 'musician',
 'custodian',
 'investment banker',
 'financier',
 'secretary of commerce',
 'secretary of labor',
 'performer',
 'legislator',
 'actor',
 'cabinetmaker',
 'carpenter',
 'servant',
 'ambassador',
 'chief of staff general',
 'rep.',
 'campaign manager',
 'jurist',
 'whig activist',
 'orderly',
 'sociologist',
 'bishop',
 'botanist',
 'sheriff',
 'chief of police',
 'firefighter',
 'cartographer',
 'lt. col.',
 'anthropologist',
 'minority leader',
 'food critic',
 'playwright',
 'cowboy',
 'first lady',
 'agriculture commissioner',
 'corporal',
 'flyer',
 'software engineer',
 'navigator',
 'businessman',
 'steward',
 'comedian',
 'grocer',
 'student activist',
 'machinist',
 'hatter',
 'babysitter',
 'waitress',
 'computer scientist',
 'tipper',
 'hockey player',
 'researcher',
 'broadcaster',
 'thinner', 'CEO']


# In[138]:


patterns_list = []
for title in job_list:
    #entity_pattern["pattern"] = title
    patterns_list.append({"label":"JOBTITLE", "pattern": title})
    #entity_pattern["pattern"] = title


# In[139]:


from spacy.pipeline import EntityRuler


# In[140]:


ruler = EntityRuler(nlp)


# In[141]:


nlp.pipeline


# In[142]:


ruler.add_patterns(patterns_list)
#nlp.remove_pipe('entity_ruler')
nlp.add_pipe(ruler)


# In[143]:


doc = None
with open('WikipediaArticles/stevejobs.txt', 'r', encoding='utf-8',errors="ignore") as file:
        content = file.read()
        doc = nlp(content)
        #relations = show_buy_relations(doc)


# In[144]:


sents = list(doc.sents)
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

spans = list(doc.ents) + list(doc.noun_chunks)
spans = filter_spans(spans)
with doc.retokenize() as retokenizer:
    for span in spans:
        retokenizer.merge(span)


# In[145]:


def get_subtree(obj, r_subtree):
    if obj.n_rights:
        r_subtree += list(obj.rights)
        for child in obj.rights:
            get_subtree(child, r_subtree)
    return r_subtree
#[w for w in token.subtree if w.dep_ == "pobj" and w.nbor(-1).text == 'by']


# In[146]:


from spacy.matcher import Matcher
pattern = [{'ENT_TYPE': 'PERSON', 'OP': '?'},
           {'IS_PUNCT': True, 'OP': '*'},
           {'ENT_TYPE': 'JOBTITLE'},
           {'IS_PUNCT': True, 'OP': '*'},
           {'ENT_TYPE': 'ORG'}]
matcher = Matcher(nlp.vocab)
matcher.add('WORK', None, pattern)


# In[156]:


def extract_work_relation(doc, file_name): 
    #doc = doc._.coref_resolved
    print('Processing template....')
    sents = list(doc.sents)
    #relation_dict = {"template": "BUY", "sentences": [], "arguments": {"1": "", "2": "", "3": "","4": "","5": ""}
    json_template = {"document": file_name, "extraction":[]}
    for sent in sents:
        main_subject = ''
        potential_subject = ''
        org = ''
        titles = []
        loc = ''
        org_flag = False
        title_flag = False
        relation_dict = {"template": "WORK", "sentences": [], "arguments": {"1": "", "2": "", "3": "","4": ""}}
        match = 0
        multi_relations = []
        for token in sent:
            #print(token)
            if token.dep_ == "nsubj":
                [w for w in token.lefts if w.dep_ == "nsubj"]
                match += 1
                main_subject = token
                r_subtree = get_subtree(main_subject.head,[])
                for child in r_subtree:
                    if child.ent_type_ == 'JOBTITLE':
                        titles.append(child.text)
                        title_flag = True
                    if child.ent_type_ == 'ORG':
                        org = child
                        org_flag = True
                    if child.ent_type_ == 'GPE':
                        loc = child 
            if token.ent_type_ == "PERSON":
                potential_subject = token
            
#             if token.text == 'of':
#                 match += 1
#                 new_rel = {}
#                 if token.nbor().ent_type_ == 'ORG':
#                     new_rel['org'] = token.nbor().text
#                 i = 0
#                 more_titles = ''
#                 while token.nbor(-i).ent_type_ == 'JOBTITLE' or token.nbor(-i).pos_ == 'CCONJ':
#                     if token.nbor(-i).ent_type_ == 'JOBTITLE':
#                         more_titles = more_titles + token.nbor(-i).text + ';'
#                     i += 1
#                 if more_titles:
#                     new_rel['title'] = more_titles
#                 if new_rel:
#                     multi_relations.append(new_rel)
        if (main_subject and main_subject.ent_type_ != 'PERSON') and potential_subject:
            main_subject = potential_subject
        if org_flag and title_flag:
            relation_dict["sentences"].append(sent.text)
            relation_dict["arguments"]["1"] = main_subject.text if main_subject else ""
            relation_dict["arguments"]["2"] = org.text if org else ""
            all_titles = ''
            for title in set(titles):
                all_titles = all_titles + title + '; '
            relation_dict["arguments"]["3"] = all_titles[0:-2] if all_titles else ''
            relation_dict["arguments"]["4"] = loc.text if loc else ""
            json_template["extraction"].append(relation_dict)
#             if multi_relations:
#                 for rel in multi_relations:
#                     #print(rel)
#                     relation_dict["arguments"]["2"] = rel['org'] if 'org' in rel else ''
#                     relation_dict["arguments"]["3"] = rel['title'][0:-2] if 'title' in rel else ''
#                     json_template["extraction"].append(relation_dict)
                #displacy.render(sent, style='dep', jupyter=True)
                #print(buy_relations[-1])
    #print(json_template)
    #return buy_relations
#     for sent in sents:
#         found_matches = matcher(nlp(sent.text))
#         if(found_matches):
#             print(found_matches)
#             for match_id, start, end in found_matches:
#                 string_id = doc.vocab.strings[match_id]  # Look up string ID
#                 span = doc[start:end]
                #print(string_id, span.text)
                #for token in span:
                    #print(token)
    print('Template processed.')                
    return json_template


# In[157]:


def create_nlpdoc_object(file_name):
    #relations = None
    with open(file_name, 'r', encoding='utf-8',errors="ignore") as file:
        content = file.read()
        doc = nlp(content)
        #relations = show_buy_relations(doc)
    return doc


# In[158]:

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
json_buy = extract_work_relation(doc, file_name)

json_file = file_name[:len(file_name)-4] + ".json"
json_object = json.loads(json.dumps(json_buy))
json_formatted_str = json.dumps(json_object, indent=4)
file = open(json_file, "a+")
n = file.write(json_formatted_str)
file.close()
print('saved to JSON')

# In[ ]:





# In[ ]:




