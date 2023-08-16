from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import searchForm
import json
from neo4j import GraphDatabase
import networkx as nx
from pyvis.network import Network
from django.conf import settings
import pandas as pd
import Cypher as c
import subprocess
from django.http import HttpResponse
import pandas as pd
import csv
import sklearn 

import os
#as scikit_learn
import scipy
import altair as alt
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.multioutput import MultiOutputClassifier
from sklearn.linear_model import SGDClassifier
from sklearn import preprocessing
from sklearn.metrics import f1_score


uri = "bolt://localhost:7687"
user = "neo4j"
password = "12345678"
driver = GraphDatabase.driver(uri, auth=(user, password))
session = driver.session(database="test")


def home(request):
    form = searchForm()
    if request.method == 'POST':
        form = searchForm(request.POST)
        if form.is_valid():
            input_data = form.cleaned_data['form_data']
            if input_data == '12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw':
                return redirect('create_graph_1')

              #     query = 'MATCH p=()-[r:PAYS]->() RETURN p LIMIT 25'
              #     result = session.run(query)
              #     data = result.data()
              #     net = Network(height="500px", width="100%")
              #     for item in data:
              #            source_index = item['p'][0]['index']
              #            target_index = item['p'][2]['index']

              #            net.add_node(source_index, color="#00FF7F")
              #            net.add_node(target_index)
              #            net.add_edge(source_index, target_index, label='PAYS',arrows='to')
              # #     net.barnes_hut()
              #     net.save_graph(str(settings.BASE_DIR)+'/lab/templates/pvis_graph_file.html')

              #     df = pd.json_normalize(data)
              #     filename = "12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw_txs_outs.json"

    context = {'form': form}
    return render(request, "lab/index.html", context=context)


def show_data1(request):
    query = 'MATCH p=()-[r:PAYS]->() RETURN p LIMIT 25'
    result = session.run(query)
    data = result.data()
    df = pd.json_normalize(data)
    html = df.to_html()

    context = {'html': html}
    return render(request, "lab/show_data1.html", context=context)


def wannacry_function(request):
    if request.method == "POST":
        return redirect("create_graph_1")
    return render(request, "lab/wannacry/wannacry.html")


def create_graph_1(request):
    c.create_graph_wannacry()
    c.update_depth()
    c.cast_depth()
    c.parse_timestamp()
    c.parse_tx()
    c.format_timestamp()
    c.format_tx()
    query = 'MATCH p=()-[r:PAYS]->() RETURN p '
    result = session.run(query)
    data = result.data()
    # G = nx.MultiDiGraph()
    # # This is how the graph currently looks with pyvis
    # # nt = Network('500px', '500px',directed=True)
    # # nt.from_nx(G)
    # # nt.show('nx.html')

    net = Network(height="500px", width="100%")
    # net.barnes_hut()
    count = 0
    for item in data:

        source_index = item['p'][0]['index']
        target_index = item['p'][2]['index']

        # G.add_node(source_index, color="#00FF7F")
        # G.add_node(target_index)
        # G.add_edge(source_index, target_index, label='PAYS',arrows='to')
        if source_index == "12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw":
            net.add_node(source_index,color='red')
        else :
            net.add_node(source_index, color="#00FF7F")
        net.add_node(target_index)
        net.add_edge(source_index, target_index, label='PAYS', arrows='to')
    # net.from_nx(G)
    # net.show("example.html")
    # net.show_buttons()
    # net.show_buttons()
    # net.nodes['12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw']['color'] = "#FF0000"

    net.save_graph(str(settings.BASE_DIR) +
                   '/lab/templates/pvis_graph_file.html')

    number_of_nodes = c.count()[0]['COUNT(n)']
    c.refresh_graph()
    number_of_relationships = c.create_graph_catalogue()[
        0]['relationshipCount']
    

    context = {'n': number_of_nodes, 'r': number_of_relationships}
    return render(request, "lab/wannacry/wannacry2.html", context=context)


def page_rank_1(request):

    pageRank = c.pageRank()
    data = json.dumps(c.set_properties_for_degree_centrality())
    context = {'data': data}

    return render(request, "lab/wannacry/page-rank.html", context=context)


def btc_txid(request):
    data = json.dumps(c.total_amount_passing_tx_node())
    context = {'data': data}
    return render(request, 'lab/wannacry/btc_txid.html', context=context)


def btc_address_node(request):
    data = json.dumps(c.total_amount_passing_address_node())
    context = {'data': data}
    return render(request, 'lab/wannacry/btc_address_node.html', context=context)


def risk_rating_tx(request):
    data = json.dumps(c.risk_rating_txt_node())
    context = {'data': data}
    return render(request, 'lab/wannacry/risk_rating_tx.html', context=context)


def risk_rating_address(request):
    data = json.dumps(c.risk_rating_address_node())
    context = {'data': data}
    print(data)
    return render(request, 'lab/wannacry/risk_rating_address.html', context=context)


def SageMaker(request):
    c.delete_graph('addresses_with_transactions_1')
    c.create_graph_catalog_for_graph_sage_model()
    c.delete_model('weightedTrainedModel')
    c.train_graph_sage_model()
    c.delete_model('testModel')
    c.test_different_hp_graph_sage()
    data = c.FastRP()
    context = {'data': data}
    print(data)

    return render(request, 'lab/wannacry/sagemaker.html', context=context)


# def run_ml_file(request):
#     try:
#         # Execute the python ML file and capture its output and error
#         output = subprocess.check_output(["python", "/Users/sankalpchordia/Desktop/Kavach/Defendify-project/lab/testpad.py"],
#                                          stderr=subprocess.STDOUT, text=True)
        
#         # Assuming that the output is in CSV format
#         # Create the HttpResponse object with the appropriate CSV header
#         response = HttpResponse(output, content_type="text/csv")
#         response["Content-Disposition"] = 'attachment; filename="output.csv"'
        
#         # Return the response directly
#         return response
#     except subprocess.CalledProcessError as e:
#         # Handle subprocess error here
#         error_message = f"Subprocess error: {e.output}"
#         return HttpResponse(error_message)


def run_ml_file(request):
        csv_file_path = os.path.join(settings.BASE_DIR, 'lab', '20210313b_GraphSAGE_embed_features_output_predictor_3.csv')
        
        csv_data = []
        
        with open(csv_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                csv_data.append(row)
        
        data = json.dumps(csv_data)
        
        print(data)

        context = [data]
        
        
       
    
        return render(request,"lab/wannacry/ml-csv.html",{'response':context})
    

    # fileName = '20210313b_GraphSAGE_embed_features'

    # d = pd.read_csv(fileName+'.csv')
    # nd = d['features'].str.strip('[]').str.split(',').apply(pd.Series)
    # X=nd

    # #TSNE
    # X_embedded = TSNE(n_components=2, random_state=6).fit_transform(X)
    # #X_embedded = TSNE(n_components=2, random_state=6).fit_transform(list(X.embedding))
    # TSNE_components = pd.DataFrame(X_embedded, columns=['X_red_X', 'X_red_Y'])
    # #TSNE_components = TSNE_components.assign(X_red_X=X_embedded[:,0], X_red_Y=X_embedded[:,1])
    # TSNE_components['btc_id']=d['name']
    # TSNE_components['risk_rating']=d['exp']
    # TSNE_components['pageRank']=d['pr']
    # TSNE_components['out_deg']=d['outdeg']
    # TSNE_components['in_deg']=d['indeg']
    # TSNE_components['total_amount']=d['ta']

    # #Reduce the components to 2
    # pca = PCA(n_components=2)
    # X_red = pca.fit_transform(X)
    # # Save components to a DataFrame
    # PCA_components = pd.DataFrame(X_red, columns=['X_red_X', 'X_red_Y'])
    # PCA_components['btc_id']=d['name']
    # PCA_components['risk_rating']=d['exp']
    # PCA_components['pageRank']=d['pr']
    # PCA_components['out_deg']=d['outdeg']
    # PCA_components['in_deg']=d['indeg']
    # PCA_components['total_amount']=d['ta']

    # def elbow_fn(X_red):
    #     ks = range(1, 10)
    #     inertias = []
    #     for k in ks:
    #         # Create a KMeans instance with k clusters: model
    #         model = KMeans(n_clusters=k)

    #         # Fit model to samples
    #         model.fit(X_red)

    #         # Append the inertia to the list of inertias
    #         inertias.append(model.inertia_)

    # #Run Elbow function to determine the number of clusters (K) for analysis
    # #using the PCA fit
    # elbow_fn(X_red)
    # #using the TSNE fit
    # #elbow_fn(X_embedded)

    # #Determine Kmeans clustering
    # K=3
    # #X_red - PCA
    # #X_embedded - TSNE
    # kmeans = KMeans(n_clusters=K, random_state=0).fit(X_red)
    # #Cluster labels
    # lab = kmeans.labels_

    # #print("*****Cluster Centers*****")
    # #print(kmeans.cluster_centers_)
    # centers = kmeans.cluster_centers_

    # d2 = d.assign(X_red_X=X_red[:,0], X_red_Y=X_red[:,1], cluster_label=lab)
    # print(d2.head())

    # #df = pd.DataFrame(np.random.randn(100, 2))
    # msk = np.random.rand(len(d2)) < 0.8
    # train = d2[msk]
    # test = d2[~msk]
    # print(len(test))
    # print(len(train))
    # print(test.head(3))

    # le = preprocessing.LabelEncoder()
    # train['features'] = le.fit_transform(train['features'])
    # train['cluster_label'] = le.fit_transform(train['cluster_label'])

    # test['features'] = le.fit_transform(test['features'])
    # test['cluster_label'] = le.fit_transform(test['cluster_label'])

    # log = MultiOutputClassifier(SGDClassifier(loss="log_loss"), n_jobs=10)
    # log.fit(train[['features']], train[['cluster_label']])

    # print(f1_score(test[['cluster_label']],
    #             log.predict(test[['features']]), average="micro"))
    # print("****Predicted Labels****")
    # #print(log.predict(test[['features']]))
    # #df_total["pred_lin_regr"] = clf.predict(Xtest)
    # test['predicted_cluster_label'] = log.predict(test[['features']])
    # print(test[['name', 'exp', 'cluster_label','predicted_cluster_label']].head(20))
    # dx = test[['name', 'exp', 'cluster_label','predicted_cluster_label']]
    # # dx.to_csv(fileName+"_output_predictor_3.csv")
    # print(dx)
