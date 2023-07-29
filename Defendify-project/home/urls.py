from . import views

from django.urls import path

urlpatterns = [
    
    path("",views.home,name="home"),
    path("wallet",views.wallet, name="wallet"),
    path("wallet/<str:wallet>", views.wallet_detail, name ="wallet-detail")
]