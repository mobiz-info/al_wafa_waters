from django.urls import path, re_path
from . import views

app_name = 'api_erp_v1_transaction'

urlpatterns = [
    re_path(r'^sales_invoices_list/$', views.sales_invoices_list),
    re_path(r'^customer_transaction/$', views.customer_transaction),
]
