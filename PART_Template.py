import sys
import os
import json
import nltk
import spacy
import networkx as nx
nltk.download('punkt')
nltk.download('wordnet')
nlp = spacy.load('en')
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from spacy import displacy
import numpy as np


def show_part_relations(file_name):
    with open("WikipediaArticles/"+file_name,'r',encoding='utf-8-sig',errors="ignore") as file:
        data=file.read()
        sentences=sent_tokenize(data)
    json_template = {"document": file_name, "extraction":[]}
    for sentence in sentences:
        part=[]
        doc = nlp(sentence)
        edges = []
        e_list={}
        nodes=[]
        tokens=[]
        part_match="False"
    
        for ent in doc.ents:
            if(ent.text=="Richardson"):
                e_list[ent.text]='GPE'
                nodes=nodes+[ent.text]
            if(ent.label_=='GPE' and e_list.get(ent.text) is None):
                e_list[ent.text]=ent.label_
                nodes=nodes+[ent.text]
            
        for token in doc:
            for child in token.children:
                if(token.text not in tokens):        
                    tokens=tokens+[token.text]
                edges.append(('{0}'.format(token.lower_),
                      '{0}'.format(child.lower_)))
        graph = nx.Graph(edges)
        digraph=nx.DiGraph(edges)
        for i in range(len(nodes)):
            for j in range(i+1,len(nodes)):
                entity1=nodes[i].lower()
                entity2=nodes[j].lower()
                if(('is' in tokens) and (nx.has_path(digraph, source='is', target=entity1)) and (nx.has_path(digraph, source='is', target=entity2))):
                    s=(entity1,entity2)
                    if s not in part:
                        part=part+[s]
                if(('are' in tokens) and (nx.has_path(digraph, source='are', target=entity1)) and (nx.has_path(digraph, source='are', target=entity2))):
                    s=(entity1,entity2)
                    if s not in part:
                        part=part+[s]
                if(('in' in tokens) and (nx.has_path(digraph, source='in', target=entity1)) and (nx.has_path(digraph, source='in', target=entity2))):
                    s=(entity1,entity2)
                    if s not in part:
                        part=part+[s]
                if((nx.has_path(graph, source=entity1, target=entity2))):
                    nodes_in_path=nx.shortest_path(graph, source=entity1, target=entity2)
                    if('is' in nodes_in_path and 'in' in nodes_in_path):
                        s=(entity1,entity2)
                        if s not in part:
                            part=part+[s]
                    if('is' in nodes_in_path and 'of' in nodes_in_path):
                        s=(entity1,entity2)
                        if s not in part:
                            part=part+[s]
                    if('in' in nodes_in_path and 'of' in nodes_in_path):
                        s=(entity1,entity2)
                        if s not in part:
                            part=part+[s]
                    if('in' in nodes_in_path and 'of' not in nodes_in_path):
                        s=(entity1,entity2)
                        if s not in part:
                            part=part+[s]
                    if('in' not in nodes_in_path and 'is' not in nodes_in_path and 'by' not in nodes_in_path and 'of' in nodes_in_path):
                        s=(entity1,entity2)
                        if s not in part:
                            part=part+[s]
                    if('are' in nodes_in_path ):
                        s=(entity1,entity2)
                        if s not in part:
                            part=part+[s]
                    if('among' in nodes_in_path):
                        s=(entity1,entity2)
                        if s not in part:
                            part=part+[s] 
        if(len(part)!=0):
            part_match="true"
        if(part_match):
            for i in range(len(part)):
                relation_dict = {"template": "PART", "sentences": [], "arguments": {"1": "", "2": ""}}
                relation_dict["sentences"].append(sentence)
                relation_dict["arguments"]["1"] = part[i][0]
                relation_dict["arguments"]["2"] = part[i][1]
                json_template["extraction"].append(relation_dict)
    return(json_template)
 

if __name__ == '__main__':

    arg_list = sys.argv
    path=str(arg_list[1])
    #path ="/Users/meghanasolleti/Documents/NLP/Project/WikipediaArticles/"
    #directory path
    merge_ents = nlp.create_pipe("merge_entities")
    nlp.add_pipe(merge_ents)
    with os.scandir(path) as directory:
        for entry in directory:
            file_name = entry.name
            #print(file_name)
            json_part = show_part_relations(file_name)
            json_file = file_name[:len(file_name)-4] + ".json"
            json_object = json.loads(json.dumps(json_part))
            json_formatted_str = json.dumps(json_object, indent=4)
            file = open('JSON/'+json_file, "a+")
            n = file.write(json_formatted_str)
            file.close()
        
