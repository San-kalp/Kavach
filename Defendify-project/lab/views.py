from django.shortcuts import render
from django.http import HttpResponse
from .forms import searchForm
import json
from neo4j import GraphDatabase
from pyvis.network import Network
from django.conf import settings




uri = "bolt://localhost:7687"
user = "neo4j"
password = "12345678"
driver = GraphDatabase.driver(uri, auth=(user, password))
session = driver.session(database="test")

# Create your views here.

def home(request):
    form = searchForm()
    if request.method =='POST':
        form = searchForm(request.POST)
        if form.is_valid():
            input_data = form.cleaned_data['form_data']
            if input_data == '12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw':
                   query = 'MATCH p=()-[r:PAYS]->() RETURN p LIMIT 25'
                   result = session.run(query)
                   data = result.data()
                   net = Network()
                   for item in data:
                          source_index = item['p'][0]['index']
                          target_index = item['p'][2]['index']
                                   
                          net.add_node(source_index)
                          net.add_node(target_index)
                          net.add_edge(source_index, target_index, label='PAYS') 
                   net.barnes_hut()
                   net.save_graph(str(settings.BASE_DIR)+'/lab/templates/pvis_graph_file.html')
            return render(request, 'lab/ss.html')


     
    context = {'form':form}
    return render(request,"lab/index.html",context=context)
#     query = 'MATCH (n) RETURN COUNT(n) AS count'
#     result = session.run(query)
#     return HttpResponse(result.data())


# def wannaCry(address):
#     query = 'MATCH p=()-[r:PAYS]->() RETURN p LIMIT 25'
#     result = session.run(query)
#     data = result.data()
#     map_data(data)

    


    






# def map_data(data,request=None):
#      net = Network(height="1500px",width="100%",bgcolor='#222222',font_color="white")
#      for item in data:
#                source_index = item['p'][0]['index']
#                target_index = item['p'][2]['index']
               
#                net.add_node(source_index)
#                net.add_node(target_index)
#                net.add_edge(source_index, target_index, label='PAYS') 
          
#      html = net.generate_html(name="ss.html")
#      return render(request,"lab/ss.html",{'html':html})

     





        #From -> item["p"][0]
        #{'in_degree': 0, 'pageRank': 0.15000000000000002, 'depth': ['0'], 'risk_rating': 7.83608898204724, 'total_amount': 17.77113036999999, 'out_degree': 112, 'index': '12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw', 'label': 'NA'}
        
        #relationship -> item["p"][1]
        #    PAYS
       
        # To -> item["p"][2] 
        # {'in_degree': 76, 'pageRank': 0.23651785714285709, 'depth': ['0'], 'time_stamp': '03/08/2017 04:41:34 UTC', 'risk_rating': 5.476845459488191, 'total_amount': 18.066477230000004, 'out_degree': 1, 'index': '35e5d5fe8c8128cfa6884f56be5817e4138c58c91b79d78d3e78a8d365b9d8a7'}










#     print(data[0]["p"][0]["in_degree"])
#     write_json(data,address)     



# def write_json(data , addr):
#     filename = addr+".json"
#     with open(filename,"w") as f :
#         json.dump(data,f,indent= 4)