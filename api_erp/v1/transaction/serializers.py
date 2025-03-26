import datetime
from django.conf import settings

from rest_framework import serializers

from master.models import *
from accounts.models import *
from client_management.models import *
from van_management.models import *
from sales_management.models import *

    
class SalesReportSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.customer_name', read_only=True)
    customer_code = serializers.CharField(source='customer.custom_id', read_only=True)
    total_supply_qty = serializers.IntegerField(source='get_total_supply_qty', read_only=True)
    net_taxable = serializers.SerializerMethodField()  
    amount_received = serializers.SerializerMethodField()  
    amount_total = serializers.SerializerMethodField()  
    invoice_type = serializers.SerializerMethodField() 
    quantity = serializers.SerializerMethodField()  
    price = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomerSupply
        fields = ['created_date', 'invoice_no', 'reference_number', 'customer_name', 'customer_code', 'amount_total', 'vat', 'discount', 'net_taxable', 'amount_received', 'total_supply_qty', 'invoice_type', 'quantity', 'price']

    def get_net_taxable(self, obj):
        return obj.net_payable

    def get_amount_received(self, obj):
        return obj.amount_recieved

    def get_amount_total(self, obj):
        return obj.subtotal
    
    def get_invoice_type(self, obj):
        if obj.amount_recieved > 0 or obj.customer.sales_type == "FOC":
            return "cash_invoice"
        elif obj.amount_recieved <= 0 and obj.customer.sales_type != "FOC":
            return "credit_invoice"
        return "all"
    
    def get_quantity(self, obj):
        return obj.get_total_supply_qty()  

    def get_price(self, obj):
        return obj.get_rate()
    

class CustomerTransactionSerializer(serializers.ModelSerializer):
    
    date = serializers.SerializerMethodField()
    ref_invoice_no = serializers.CharField(source='customer_supply.reference_number', read_only=True)
    invoice_number = serializers.CharField(source='customer_supply.invoice_no', read_only=True)
    product_name = serializers.CharField(source='product.product_name', read_only=True)
    sales_type = serializers.CharField(source='customer_supply.customer.sales_type', read_only=True)
    qty = serializers.IntegerField(source='quantity', read_only=True)
    amount = serializers.DecimalField(source='customer_supply.grand_total', max_digits=10, decimal_places=2, read_only=True)
    discount = serializers.DecimalField(source='customer_supply.discount', max_digits=10, decimal_places=2, read_only=True)
    net_taxable = serializers.DecimalField(source='customer_supply.subtotal', max_digits=10, decimal_places=2, read_only=True)
    vat_amount = serializers.DecimalField(source='customer_supply.vat', max_digits=10, decimal_places=2, read_only=True)
    grand_total = serializers.DecimalField(source='customer_supply.grand_total', max_digits=10, decimal_places=2, read_only=True)
    amount_collected = serializers.DecimalField(source='customer_supply.amount_recieved', max_digits=10, decimal_places=2, read_only=True)

    salesman = serializers.CharField(source='customer_supply.salesman.username', read_only=True)
    van = serializers.SerializerMethodField()
    location = serializers.CharField(source='customer_supply.customer.location', read_only=True)
    receipt_no = serializers.SerializerMethodField()
    receipt_date = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = CustomerSupplyItems
        fields = [
            'date', 'ref_invoice_no', 'invoice_number', 'product_name', 'sales_type', 'qty', 'amount', 'discount', 
            'net_taxable', 'vat_amount', 'grand_total', 'amount_collected', 'salesman', 'van', 'location', 
            'receipt_no', 'receipt_date', 'status'
        ]

    def get_date(self, obj):
        return obj.customer_supply.created_date.date() if obj.customer_supply.created_date else None

    def get_van(self, obj):
        if obj.customer_supply.salesman and obj.customer_supply.salesman.salesman_van.exists():
            return obj.customer_supply.salesman.salesman_van.first().van_make
        return None

    def get_receipt_no(self, obj):
        receipt = Receipt.objects.filter(invoice_number=obj.customer_supply.invoice_no).first()
        return receipt.receipt_number if receipt else None

    def get_receipt_date(self, obj):
        receipt = Receipt.objects.filter(invoice_number=obj.customer_supply.invoice_no).first()
        return receipt.created_date.date() if receipt else None

    def get_status(self, obj):
        return "Paid" if obj.customer_supply.amount_recieved >= obj.customer_supply.grand_total else "Pending"
    
    
class CustomerCouponSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    ref_invoice_no = serializers.CharField(source='customer_coupon.reference_number', read_only=True)
    invoice_number = serializers.CharField(source='customer_coupon.invoice_no', read_only=True)
    product_name = serializers.CharField(source='coupon.book_num', read_only=True)
    sales_type = serializers.CharField(source='customer_coupon.customer.sales_type', read_only=True)
    qty = serializers.IntegerField(default=1)
    amount = serializers.DecimalField(source='customer_coupon.grand_total', max_digits=10, decimal_places=2, read_only=True)
    discount = serializers.DecimalField(source='customer_coupon.discount', max_digits=10, decimal_places=2, read_only=True)
    net_taxable = serializers.DecimalField(source='customer_coupon.net_amount', max_digits=10, decimal_places=2, read_only=True)
    vat_amount = serializers.DecimalField(default=0, max_digits=10, decimal_places=2, read_only=True)
    grand_total = serializers.DecimalField(source='customer_coupon.grand_total', max_digits=10, decimal_places=2, read_only=True)
    amount_collected = serializers.DecimalField(source='customer_coupon.amount_recieved', max_digits=10, decimal_places=2, read_only=True)
    salesman = serializers.CharField(source='customer_coupon.salesman.username', read_only=True)
    van = serializers.SerializerMethodField()
    location = serializers.CharField(source='customer_coupon.customer.location', read_only=True)
    receipt_no = serializers.SerializerMethodField()
    receipt_date = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = CustomerCouponItems
        fields = [
            'date', 'ref_invoice_no', 'invoice_number', 'product_name', 'sales_type', 'qty', 'amount', 'discount', 
            'net_taxable', 'vat_amount', 'grand_total', 'amount_collected', 'salesman', 'van', 'location', 
            'receipt_no', 'receipt_date', 'status'
        ]

    def get_date(self, obj):
        return obj.customer_coupon.created_date.date() if obj.customer_coupon.created_date else None

    def get_van(self, obj):
        if obj.customer_coupon.salesman and obj.customer_coupon.salesman.salesman_van.exists():
            return obj.customer_coupon.salesman.salesman_van.first().van_make
        return None

    def get_receipt_no(self, obj):
        receipt = Receipt.objects.filter(invoice_number=obj.customer_coupon.invoice_no).first()
        return receipt.receipt_number if receipt else None

    def get_receipt_date(self, obj):
        receipt = Receipt.objects.filter(invoice_number=obj.customer_coupon.invoice_no).first()
        return receipt.created_date.date() if receipt else None

    def get_status(self, obj):
        return "Paid" if obj.customer_coupon.amount_recieved >= obj.customer_coupon.grand_total else "Pending"
