import requests
import datetime
from decimal import Decimal
from datetime import datetime

from django.contrib.auth.models import User
from django.db.models import Q, Sum, Min, Max
from django.shortcuts import get_object_or_404
from django.db import transaction, IntegrityError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, renderer_classes

from master.models import BranchMaster, DesignationMaster, EmirateMaster, LocationMaster, RouteMaster
from accounts.models import CustomUser, Customers
from client_management.models import *
from van_management.models import *

from api_erp.v1.transaction.serializers import *


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@renderer_classes([JSONRenderer])
def sales_invoices_list(request):
    start_date = request.GET.get('start_date', datetime.today().date())
    end_date = request.GET.get('end_date', datetime.today().date())
    sales_type = request.GET.get('invoice_types')  
    route_name = request.GET.get('route_id')
    customer_id = request.GET.get('customer_id')

    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    try:
        route = Van_Routes.objects.get(van__salesman=request.user).routes
        is_salesman = True
    except Van_Routes.DoesNotExist:
        route = None
        is_salesman = False
    
    sales_filter = {
        "created_date__date__gte": start_date,
        "created_date__date__lte": end_date,
    }

    if is_salesman:
        sales_filter["customer__routes"] = route
    elif route_name:
        sales_filter["customer__routes"] = route_name
    else:
        all_routes = Van_Routes.objects.values_list("routes", flat=True)
        sales_filter["customer__routes__in"] = all_routes

    if customer_id:
        sales_filter["customer__customer_id"] = customer_id

    if sales_type == "cash_invoice":
        sales = CustomerSupply.objects.filter(
            Q(amount_recieved__gt=0) | Q(customer__sales_type="FOC"),
            **sales_filter
        )
    elif sales_type == "credit_invoice":
        sales = CustomerSupply.objects.filter(
            amount_recieved__lte=0,
            **sales_filter
        ).exclude(customer__sales_type="FOC")
    else:
        sales = CustomerSupply.objects.filter(**sales_filter)

    total_sales = sales.aggregate(
        total_grand_total=Sum('grand_total'),
        total_vat=Sum('vat'),
        total_net_payable=Sum('net_payable'),
        total_amount_received=Sum('amount_recieved')
    )

    response_data = {
        "StatusCode": 200,
        "status": "success",
        "data": {
            "invoices": SalesReportSerializer(sales, many=True).data,
            "total_amount": round(total_sales.get("total_grand_total") or 0, 2),
            "total_vat": round(total_sales.get("total_vat") or 0, 2),
            "total_taxable": round(total_sales.get("total_net_payable") or 0, 2),
            "total_amount_collected": round(total_sales.get("total_amount_received") or 0, 2),
            "filters": {
                "route_name": str(route) if route else "All Routes",
                "invoice_types": sales_type if sales_type else "All", 
                "start_date": str(start_date),
                "end_date": str(end_date),
                "customer_id": customer_id if customer_id else "All"
            }
        },
    }
    return Response(response_data, status=200)


@api_view(['GET'])
@permission_classes([AllowAny])
@renderer_classes([JSONRenderer])
def customer_transaction(request):
    customer_pk = request.GET.get("customer_id")  
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    transaction_type = request.GET.get('transaction_type')  

    sales = CustomerSupplyItems.objects.exclude(
        customer_supply__customer__sales_type__in=["CASH COUPON", "CREDIT COUPON"]
    ).order_by('-customer_supply__created_date')

    coupons = CustomerCouponItems.objects.all()
    collections = CollectionPayment.objects.all()

    if customer_pk:
        sales = sales.filter(customer_supply__customer__pk=customer_pk)
        coupons = coupons.filter(customer_coupon__customer__pk=customer_pk)
        collections = collections.filter(customer__pk=customer_pk)

    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            sales = sales.filter(customer_supply__created_date__date__range=(start_date, end_date))
            coupons = coupons.filter(customer_coupon__created_date__date__range=(start_date, end_date))
            collections = collections.filter(created_date__date__range=(start_date, end_date))
        except ValueError:
            return Response({"StatusCode": 4001, "message": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)

    customers = Customers.objects.filter(pk=customer_pk) if customer_pk else Customers.objects.all()

    transactions = []

    for customer in customers:
        customer_id = customer.customer_id
        custom_id = customer.custom_id
        customer_name = customer.customer_name
        customer_sales = sales.filter(customer_supply__customer=customer)
        customer_coupons = coupons.filter(customer_coupon__customer=customer)
        customer_collections = collections.filter(customer=customer)

        if not transaction_type or transaction_type == "supply":
            transactions += [
                {
                    "transaction_type": "supply",
                    "customer_id": customer_id,
                    "custom_id": custom_id,
                    "customer_name": customer_name,
                    "products": [
                        {
                            "product_name": item.product.product_name,
                            "quantity": item.quantity,
                            "amount": item.customer_supply.grand_total
                        }
                        for item in customer_sales
                    ],
                    **data
                } 
                for data in CustomerTransactionSerializer(customer_sales, many=True).data
            ]

        if not transaction_type or transaction_type == "coupon_recharge":
            transactions += [
                {
                    "transaction_type": "coupon_recharge",
                    "customer_id": customer_id,
                    "custom_id": custom_id,
                    "customer_name": customer_name,
                    **data
                } 
                for data in CustomerCouponSerializer(customer_coupons, many=True).data
            ]

        if not transaction_type or transaction_type == "collection":
            transactions += [
                {
                    "transaction_type": "collection",
                    "customer_id": customer_id,
                    "custom_id": custom_id,
                    "customer_name": customer_name,
                    "collection_id": col.id,
                    "amount_collected": col.amount_received,
                    "collection_date": col.created_date.date() if col.created_date else None,
                    "receipt_number": col.receipt_number,
                    "payment_method": col.payment_method,
                    "salesman": col.salesman.username if col.salesman else None,
                    "total_amount": col.total_amount(),
                    "total_discount": col.total_discounts(),
                    "total_net_taxable": col.total_net_taxeble(),
                    "total_vat": col.total_vat(),
                    "collected_amount": col.collected_amount(),
                    "is_repeated_customer": col.is_repeated_customer(),
                    "invoices": [
                        {
                            "invoice_number": item.invoice.invoice_no,
                            "amount": item.amount,
                            "balance": item.balance,
                            "amount_received": item.amount_received
                        }
                        for item in CollectionItems.objects.filter(collection_payment=col)
                    ]
                }
                for col in customer_collections
            ]

    response_data = {
        "StatusCode": 6000,
        "status": status.HTTP_200_OK,
        "transactions": transactions,
    }

    return Response(response_data, status=status.HTTP_200_OK)