from django.urls import path, re_path
from . import views

app_name = 'api_erp_v1_master'

urlpatterns = [
    re_path(r'^route/$', views.routes),
    re_path(r'^branch/$', views.branch),
    re_path(r'^emirate/$', views.emirate),
    re_path(r'^designation/$', views.designation),
    re_path(r'^location/$', views.location),
    re_path(r'^users/$', views.user_list),
    re_path(r'^customer/$', views.customer),
    re_path(r'^product-items/$', views.product_item_list),
    re_path(r'^van/$', views.van),
    
]
