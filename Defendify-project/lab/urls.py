from . import views


from django.urls import path

urlpatterns = [
    
    path("",views.home,name="home"),
    path("show_data1",views.show_data1,name="show_data1"),
    path("/12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw/",views.wannacry_function,name="wannacry"),
    path("/12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw/create-graph",views.create_graph_1,name="create_graph_1"),
    path("/12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw/page-rank",views.page_rank_1,name="page_rank_1"),
    path("btc-txid",views.btc_txid,name="btc_txid"),
    path("btc-address-node",views.btc_address_node,name="btc_address_node"),
    path("risk-rating-tx",views.risk_rating_tx,name="risk_rating_tx"),
    path("risk-rating-address",views.risk_rating_address,name="risk_rating_address"),
    path("sagemaker",views.SageMaker,name='SageMaker'),


   
  
]