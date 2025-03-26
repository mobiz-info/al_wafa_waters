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

from api_erp.v1.master.serializers import *


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def routes(request):
    route_id = request.GET.get('route_id')
    many=True
    
    instances = RouteMaster.objects.all()
    
    if route_id:
        instances = instances.filter(pk=route_id).first()
        many=False
        
    serializer = RouteMasterSerializer(instances,many=many)
    
    status_code = status.HTTP_200_OK
    response_data = {
        "StatusCode": 6000,
        "status": status_code,
        "data": serializer.data
    }

    return Response(response_data, status_code)


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def branch(request):
    branch_id = request.GET.get('branch_id')
    many=True
    
    instances = BranchMaster.objects.all()
    
    if branch_id:
        instances = instances.filter(pk=branch_id).first()
        many=False
        
    serializer = BranchMasterSerializer(instances,many=many)
    
    status_code = status.HTTP_200_OK
    response_data = {
        "StatusCode": 6000,
        "status": status_code,
        "data": serializer.data
    }

    return Response(response_data, status_code)


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def emirate(request):
    emirate_id = request.GET.get('emirate_id')
    many=True
    
    instances = EmirateMaster.objects.all()
    
    if emirate_id:
        instances = instances.filter(pk=emirate_id).first()
        many=False
        
    serializer = EmirateMasterSerializer(instances,many=many)
    
    status_code = status.HTTP_200_OK
    response_data = {
        "StatusCode": 6000,
        "status": status_code,
        "data": serializer.data
    }

    return Response(response_data, status_code)


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def designation(request):
    designation_id = request.GET.get('designation_id')
    many=True
    
    instances = DesignationMaster.objects.all()
    
    if designation_id:
        instances = instances.filter(pk=designation_id).first()
        many=False
        
    serializer = DesignationMasterSerializer(instances,many=many)
    
    status_code = status.HTTP_200_OK
    response_data = {
        "StatusCode": 6000,
        "status": status_code,
        "data": serializer.data
    }

    return Response(response_data, status_code)


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def location(request):
    location_id = request.GET.get('location_id')
    many=True
    
    instances = LocationMaster.objects.all()
    
    if location_id:
        instances = instances.filter(pk=location_id).first()
        many=False
        
    serializer = LocationMasterSerializer(instances,many=many)
    
    status_code = status.HTTP_200_OK
    response_data = {
        "StatusCode": 6000,
        "status": status_code,
        "data": serializer.data
    }

    return Response(response_data, status_code)


@api_view(['GET'])
@permission_classes([AllowAny])
@renderer_classes([JSONRenderer])
def user_list(request):
    user_id = request.GET.get('user_id')
    many = True

    users = CustomUser.objects.all()

    if user_id:
        users = users.filter(pk=user_id).first()
        many = False

    serializer = CustomUserSerializer(users, many=many)

    response_data = {
        "StatusCode": 6000,
        "status": status.HTTP_200_OK,
        "data": serializer.data
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def customer(request):
    customer_id = request.GET.get('customer_id')
    many=True
   
    instances = Customers.objects.all()
   
    if customer_id:
        instances = instances.filter(pk=customer_id).first()
        many=False
       
    serializer = CustomersSerializer(instances,many=many)
   
    status_code = status.HTTP_200_OK
    response_data = {
        "StatusCode": 6000,
        "status": status_code,
        "data": serializer.data
    }


    return Response(response_data, status_code)


@api_view(['GET'])
@permission_classes([AllowAny])
@renderer_classes([JSONRenderer])
def product_item_list(request):
    product_id = request.GET.get('product_id')
    many = True

    products = ProdutItemMaster.objects.all()

    if product_id:
        products = products.filter(pk=product_id).first()
        many = False

    serializer = ProdutItemMasterSerializer(products, many=many)

    response_data = {
        "StatusCode": 6000,
        "status": status.HTTP_200_OK,
        "data": serializer.data
    }

    return Response(response_data, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([AllowAny])
@renderer_classes([JSONRenderer])
def van(request):
    van_id = request.GET.get('van_id')
    many = True

    vans = Van.objects.all()

    if van_id:
        vans = vans.filter(van_id=van_id).first()
        many = False

    serializer = VanSerializers(vans, many=many)

    response_data = {
        "StatusCode": 6000,
        "status": status.HTTP_200_OK,
        "data": serializer.data
    }

    return Response(response_data, status=status.HTTP_200_OK)


