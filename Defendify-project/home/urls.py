from . import views

from django.urls import path

urlpatterns = [
    
    path("",views.home,name="home"),
    path("wallet",views.wallet, name="wallet"),
    path("wallet/<str:wallet>", views.wallet_detail, name ="wallet-detail"),
    path("wallet/<str:wallet>/transactions",views.wallet_transactions,name ="wallet_transactions"),
    path("QR-code",views.qr_code,name="qr_code"),
    path("regex",views.handle_regex,name = "handle_regex"),
]