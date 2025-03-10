import datetime
from django.core.management.base import BaseCommand
from accounts.models import CustomUser, Customers
from client_management.models import CustodyCustom, Customer_Inhand_Coupons, CustomerCart, CustomerCoupon, CustomerCouponStock, CustomerCustodyStock, CustomerOrders, CustomerOutstanding, CustomerOutstandingReport, CustomerReturn, CustomerSupply, CustomerSupplyStock, DialyCustomers, NonvisitReport, OutstandingAmount, Vacation
from coupon_management.models import CouponLeaflet, FreeLeaflet, NewCoupon
from customer_care.models import CouponPurchaseModel, CustodyPullOutModel, CustomerComplaint, DiffBottlesModel, OtherRequirementModel
from invoice_management.models import Invoice
from order.models import ChangeOrReturn, Customer_Order
from sales_management.models import CollectionPayment, CustomerCoupons, OutstandingLog, SaleEntryLog, SalesmanSpendingLog, Transaction, Transactionn
from van_management.models import CustomerProductReplace, CustomerProductReturn
from django.db.models import Count,Sum

class Command(BaseCommand):
    help = 'Generate usernames and passwords for customers based on their name and mobile number'

    def handle(self, *args, **kwargs):
        # for customer in customers:
        #     if customer.user_id:
        #         CustomUser.objects.filter(pk=customer.user_id.pk).delete()
        # customers.delete()
        
        
        Invoice.objects.filter().delete()
        CustomerOutstanding.objects.filter().delete()
        CustomerOutstandingReport.objects.filter().delete()
        CustodyCustom.objects.filter().delete()
        CustomerCustodyStock.objects.filter().delete()
        CustodyPullOutModel.objects.filter().delete()
        CustomerReturn.objects.filter().delete()
        Customer_Inhand_Coupons.objects.filter().delete()
        CustomerCoupon.objects.filter().delete()
        CustomerCouponStock.objects.filter().delete()
        CustomerSupply.objects.filter().delete()
        CustomerSupplyStock.objects.filter().delete()
        CustomerOrders.objects.filter().delete()
        NonvisitReport.objects.filter().delete()
        CustomerCart.objects.filter().delete()
        DialyCustomers.objects.filter().delete()
        
        Vacation.objects.filter().delete()
        DiffBottlesModel.objects.filter().delete()
        OtherRequirementModel.objects.filter().delete()
        CouponPurchaseModel.objects.filter().delete()
        CustomerComplaint.objects.filter().delete()
        Customer_Order.objects.filter().delete()
        # ChangeOrReturn.objects.filter().delete()
        SaleEntryLog.objects.filter().delete()
        OutstandingLog.objects.filter().delete()
        Transaction.objects.filter().delete()
        CustomerCoupons.objects.filter().delete()
        Transactionn.objects.filter().delete()
        CollectionPayment.objects.filter().delete()
        SalesmanSpendingLog.objects.filter().delete()
        CustomerProductReturn.objects.filter().delete()
        CustomerProductReplace.objects.filter().delete()
        CustomerProductReplace.objects.filter().delete()
       
        # coupon_instance = NewCoupon.objects.get(pk="fc4c8f18-dd2d-40a4-a75f-70d01d53a28a")
        # CouponLeaflet.objects.filter(coupon=coupon_instance).update(used=True)
        # FreeLeaflet.objects.filter(coupon=coupon_instance).update(used=True)
        customers_ids = Customers.objects.filter().delete()
        
