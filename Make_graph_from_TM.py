def make_graph_big(method, k):

    from TM import Topic_Model
    from gensim import corpora
    import ast
    import json
    import warnings
    import random
    from googletrans import Translator
    translator = Translator()
    warnings.filterwarnings('ignore')

    dictionary = corpora.Dictionary.load('/home/likich/TM_graph/dictionary')
    corpus = corpora.MmCorpus('/home/likich/TM_graph/corpus')  

    # print('Please choose either BERT or LDA')

    # method = input()

    # print('Please choose the number of topics.')

    # k = input()

    number_of_colors = 1000
    color_pallette = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                for i in range(number_of_colors)]


    if method == 'BERT':

        tm = Topic_Model(k = int(k), method = 'BERT')
        model_res = tm.fit(corpus, dictionary, cluster_model='hdbscan')
        nodes = []
        links = []
        for key, values in model_res.items():
            if key == -1:
                pass
            else:
                for tupl in values:
                    nodes.append({'name': tupl[0]})
        nodes_str = []
        for i in nodes:
            nodes_str.append(str(i))
        nodes_str = list(set(nodes_str))
        clear_nodes = []
        for i in nodes_str:
            clear_nodes.append(ast.literal_eval(i))
        node_namings_only = []
        for node in clear_nodes:
            for key, node_name in node.items():
                node_namings_only.append(node_name)
        links = []
        color_nodes = []
        for node in clear_nodes:
            for key, node_name in node.items():
                c=random.choice(color_pallette)
                for k,v in model_res.items():
                    if k == -1:
                        pass
                    else:
                        for tupl_id in range(len(v)):
                            if  v[0][0] == node_name:
                                links.append( {"source":node_namings_only.index(v[0][0]), 'target': node_namings_only.index(v[tupl_id][0]), 'color':c})         

        clear_links = []
        for i in range(len(links)):
            compare = []
            for k,v in links[i].items():
                compare.append(v)
            if compare[0] == compare[1]:
                pass
            else:
                clear_links.append(links[i])

        dict_json = {'links': clear_links, 'nodes': clear_nodes}
        with open('graph.json', 'w', encoding='utf-8') as file:
            json.dump(dict_json, file, ensure_ascii=False)

    elif method == 'LDA':
        tm1 = Topic_Model(k = int(k), method = 'LDA')
        model_res, to_show = tm1.fit(corpus, dictionary)
        nodes = []
        links = []
        color_nodes = []
        for topic in model_res:
            for word in topic:
                nodes.append({'name': word})
        nodes_str = []
        for i in nodes:
            nodes_str.append(str(i))
        nodes_str = list(set(nodes_str))
        clear_nodes = []
        for i in nodes_str:
            clear_nodes.append(ast.literal_eval(i))
        node_namings_only = []
        for node in clear_nodes:
            for key, node_name in node.items():
                
                node_namings_only.append(node_name)
        
        for node in clear_nodes:
            for key, node_name in node.items():
                c=random.choice(color_pallette)
                #print(node_name)
                for topic in model_res:
                    for word_id in range(len(topic)):
                        if  topic[0] == node_name:
                            links.append( {"source":node_namings_only.index(topic[0]), 'target': node_namings_only.index(topic[word_id]), 'color':c})         
        #убираем одинаковые сурс и таргет
        clear_links = []
        for i in range(len(links)):
            compare = []
            for k,v in links[i].items():
                compare.append(v)
            if compare[0] == compare[1]:
                pass
            else:
                clear_links.append(links[i])

        #Translation module
        
        eng_nodes = []
        for tupl in clear_nodes:
            for key, items in tupl.items():
                smol_dict = {'name': translator.translate(items).text}
                eng_nodes.append(smol_dict)





        dict_json = {'links': clear_links, 'nodes': eng_nodes}
        with open('graph.json', 'w', encoding='utf-8') as file:
            json.dump(dict_json, file, ensure_ascii=False)
     


    print('Everything is ready. Please run the command: python3 -m http.server and go to your localhost.')
  
    