from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import searchForm
import json
from neo4j import GraphDatabase
from pyvis.network import Network
from django.conf import settings
import pandas as pd
import Cypher as c



uri = "bolt://localhost:7687"
user = "neo4j"
password = "rajat123"
driver = GraphDatabase.driver(uri, auth=(user, password))
session = driver.session(database="neo4j")



def home(request):
    form = searchForm()
    if request.method =='POST':
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
              
                           
              
     
    context = {'form':form}
    return render(request,"lab/index.html",context=context)


def show_data1(request):
      query = 'MATCH p=()-[r:PAYS]->() RETURN p LIMIT 25'
      result = session.run(query)
      data = result.data()
      df = pd.json_normalize(data)
      html = df.to_html()

      context = {'html':html}
      return render(request,"lab/show_data1.html",context=context)



def wannacry_function(request):
      if request.method == "POST":
           return redirect("create_graph_1")
      return render(request,"lab/wannacry/wannacry.html")


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
     print (data)
     net = Network(height="500px", width="100%")
     for item in data:
          source_index = item['p'][0]['index']
          target_index = item['p'][2]['index']
                                   
          net.add_node(source_index, color="#00FF7F")
          net.add_node(target_index)
          net.add_edge(source_index, target_index, label='PAYS',arrows='to') 
               #     net.barnes_hut()
     net.save_graph(str(settings.BASE_DIR)+'/lab/templates/pvis_graph_file.html')
     number_of_nodes = c.count()[0]['COUNT(n)']
     c.refresh_graph()
     number_of_relationships = c.create_graph_catalogue()[0]['relationshipCount']

     context = {'n':number_of_nodes,'r':number_of_relationships}
     return render(request,"lab/wannacry/wannacry2.html",context=context)

     
def page_rank_1(request):

     pageRank = c.pageRank()
     data = json.dumps(c.set_properties_for_degree_centrality())
     context = {'data':data}

     return render(request,"lab/wannacry/page-rank.html",context=context)

def btc_txid(request):
     data = json.dumps(c.total_amount_passing_tx_node())
     context = {'data':data}
     return render(request,'lab/wannacry/btc_txid.html',context=context)
      


def btc_address_node(request):
     data = json.dumps(c.total_amount_passing_address_node())
     context = {'data':data}
     return render(request,'lab/wannacry/btc_address_node.html',context=context)

def risk_rating_tx(request):
     data = json.dumps(c.risk_rating_txt_node())
     context = {'data':data}
     return render(request,'lab/wannacry/risk_rating_tx.html',context=context)


def risk_rating_address(request):
     data = json.dumps(c.risk_rating_address_node())
     context = {'data':data}
     print(data)
     return render(request,'lab/wannacry/risk_rating_address.html',context=context)

def SageMaker(request):
     c.delete_graph('addresses_with_transactions_1')
     c.create_graph_catalog_for_graph_sage_model()
     c.delete_model('weightedTrainedModel')
     c.train_graph_sage_model()
     c.delete_model('testModel')
     c.test_different_hp_graph_sage()
     data = c.FastRP()
     context = {'data':data}
     
     return render(request,'lab/wannacry/sagemaker.html',context=context)



