import datetime
from django.conf import settings

from rest_framework import serializers

from master.models import *
from accounts.models import *
from client_management.models import *
from van_management.models import *

class RouteMasterSerializer(serializers.ModelSerializer):
    branch_name = serializers.SerializerMethodField()
    
    class Meta:
        model = RouteMaster
        fields = ['route_id','route_name','branch_id','branch_name']
        
    def get_branch_name(self,obj):
        return obj.branch_id.name
    
    
class BranchMasterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BranchMaster
        fields = ['branch_id','name','address','mobile','landline','phone','fax','trn','website','emirate','email','user_id','logo']
        
        
class EmirateMasterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EmirateMaster
        fields = ['emirate_id','name']
        
        
class DesignationMasterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DesignationMaster
        fields = ['designation_id','designation_name']
        
        
class LocationMasterSerializer(serializers.ModelSerializer):
    emirate_name = serializers.SerializerMethodField()
    emirate_id = serializers.PrimaryKeyRelatedField(source='emirate', read_only=True)
    
    class Meta:
        model = LocationMaster
        fields = ['location_id','location_name','emirate_name','emirate_id']
        
    def get_emirate_name(self, obj):
        return obj.emirate.name if obj.emirate else None

class CustomUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'user_type', 'branch_id', 'designation_id', 'staff_id', 
            'phone', 'blood_group', 'permanent_address', 'present_address', 'labour_card_no', 
            'labour_card_expiry', 'driving_licence_no', 'driving_licence_expiry', 'licence_issued_by', 
            'visa_issued_by', 'visa_no', 'visa_expiry', 'emirates_id_no', 'emirates_expiry', 
            'health_card_no', 'health_card_expiry', 'base_salary', 'wps_percentage', 'wps_ref_no', 
            'insurance_no', 'insurance_expiry', 'insurance_company', 'user_management', 
            'product_management', 'masters', 'van_management', 'coupon_management', 
            'client_management', 'nationality', 'visa_type', 'joining_date', 'passport_expiry', 
            'passport_number', 'full_name'
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}" if obj.first_name and obj.last_name else obj.username

class CustomersSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    sales_staff_name = serializers.SerializerMethodField()
    routes_name = serializers.SerializerMethodField()
    location_name = serializers.SerializerMethodField()
    emirate_name = serializers.SerializerMethodField()
    branch_name = serializers.SerializerMethodField()

    class Meta:
        model = Customers
        fields = [
            'customer_id', 'created_date', 'created_by', 'custom_id', 'customer_name', 'building_name',
            'door_house_no', 'floor_no', 'sales_staff', 'sales_staff_name', 'routes', 'routes_name', 'location', 'location_name',
            'emirate', 'emirate_name', 'mobile_no', 'whats_app', 'email_id', 'gps_latitude', 'gps_longitude',
            'customer_type', 'sales_type', 'no_of_bottles_required', 'max_credit_limit', 'credit_days',
            'no_of_permitted_invoices', 'trn', 'billing_address', 'preferred_time', 'branch_id','branch_name', 'is_active',
            'visit_schedule', 'is_editable', 'user_id', 'rate', 'coupon_count', 'five_g_count_limit',
            'eligible_foc', 'is_calling_customer', 'is_deleted', 'gps_module_active'
        ]
    def get_sales_staff_name(self, obj):
        return obj.sales_staff.get_fullname() if obj.sales_staff else None


    def get_routes_name(self, obj):
        return obj.routes.route_name if obj.routes else None


    def get_location_name(self, obj):
        return obj.location.location_name if obj.location else None


    def get_emirate_name(self, obj):
        return obj.emirate.name if obj.emirate else None
    
    def get_branch_name(self, obj):
        return obj.branch_id.name if obj.branch_id else None
    


class ProdutItemMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProdutItemMaster
        fields = [
            'id', 'product_name', 'category', 'unit', 'tax', 'rate', 'image'
        ] 
        
        
class VanSerializers(serializers.ModelSerializer):
    total_vanstock = serializers.SerializerMethodField()
    van_route = serializers.SerializerMethodField()
    
    class Meta:
        model = Van
        fields = [
            'van_id','van_make', 'plate', 'renewal_date', 'insurance_expiry_date', 'capacity',
            'bottle_count', 'driver', 'salesman', 'branch_id', 'van_type',
            'total_vanstock', 'van_route'
        ]
    
    def get_total_vanstock(self, obj):
        request = self.context.get('request')
        date = request.query_params.get('date') if request else None
        return obj.get_total_vanstock(date)
    
    def get_van_route(self, obj):
        return obj.get_van_route()
    
            
