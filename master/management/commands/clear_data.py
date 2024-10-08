import datetime
from django.core.management.base import BaseCommand
from accounts.models import CustomUser, Customers
from client_management.models import CustodyCustom, Customer_Inhand_Coupons, CustomerCart, CustomerCoupon, CustomerCouponStock, CustomerCustodyStock, CustomerOrders, CustomerOutstanding, CustomerOutstandingReport, CustomerReturn, CustomerSupply, CustomerSupplyStock, DialyCustomers, NonvisitReport, Vacation
from customer_care.models import CouponPurchaseModel, CustodyPullOutModel, CustomerComplaint, DiffBottlesModel, OtherRequirementModel
from invoice_management.models import Invoice
from order.models import ChangeOrReturn, Customer_Order
from sales_management.models import CollectionPayment, CustomerCoupons, OutstandingLog, SaleEntryLog, SalesmanSpendingLog, Transaction, Transactionn
from van_management.models import CustomerProductReplace, CustomerProductReturn

class Command(BaseCommand):
    help = 'Generate usernames and passwords for customers based on their name and mobile number'

    def handle(self, *args, **kwargs):
        customers_ids = Customers.objects.filter(routes__route_name="S-17").values_list('pk')
        # for customer in customers:
        #     if customer.user_id:
        #         CustomUser.objects.filter(pk=customer.user_id.pk).delete()
        # customers.delete()
        
        # outstanding_in = CustomerOutstanding.objects.filter(created_date__date__lte=datetime.datetime.strptime("2024-09-22", '%Y-%m-%d').date(),customer__routes__route_name="S-41")
        # Invoice.objects.filter(created_date__date__lte=datetime.datetime.strptime("2024-09-22", '%Y-%m-%d').date(),customer__routes__route_name="S-41").delete()
        # outstanding_in.delete()
        # # CustomerOutstandingReport.objects.filter(created_date__date__lte=datetime.datetime.strptime("2024-09-22", '%Y-%m-%d').date(),customer__routes__route_name="S-41").delete()
        # CollectionPayment.objects.filter(created_date__date__lte=datetime.datetime.strptime("2024-09-22", '%Y-%m-%d').date(),customer__routes__route_name="S-41").delete()
        
        Invoice.objects.filter(customer__pk__in=customers_ids).delete()
        
        CustomerOutstanding.objects.filter(customer__pk__in=customers_ids).delete()
        CustomerOutstandingReport.objects.filter(customer__pk__in=customers_ids).delete()
        CustodyCustom.objects.filter(customer__pk__in=customers_ids).delete()
        CustomerCustodyStock.objects.filter(customer__pk__in=customers_ids).delete()
        CustodyPullOutModel.objects.filter(customer__pk__in=customers_ids).delete()
        CustomerReturn.objects.filter(customer__pk__in=customers_ids).delete()
        Customer_Inhand_Coupons.objects.filter(customer__pk__in=customers_ids).delete()
        CustomerCoupon.objects.filter(customer__pk__in=customers_ids).delete()
        CustomerCouponStock.objects.filter(customer__pk__in=customers_ids).delete()
        CustomerSupply.objects.filter(customer__pk__in=customers_ids).delete()
        CustomerSupplyStock.objects.filter(customer__pk__in=customers_ids).delete()
        CustomerOrders.objects.filter(customer__pk__in=customers_ids).delete()
        NonvisitReport.objects.filter(customer__pk__in=customers_ids).delete()
        CustomerCart.objects.filter(customer__pk__in=customers_ids).delete()
        DialyCustomers.objects.filter(customer__pk__in=customers_ids).delete()
        
        Vacation.objects.filter(customer__pk__in=customers_ids).delete()
        DiffBottlesModel.objects.filter(customer__pk__in=customers_ids).delete()
        OtherRequirementModel.objects.filter(customer__pk__in=customers_ids).delete()
        CouponPurchaseModel.objects.filter(customer__pk__in=customers_ids).delete()
        CustomerComplaint.objects.filter(customer__pk__in=customers_ids).delete()
        Customer_Order.objects.filter(customer_id__pk__in=customers_ids).delete()
        # ChangeOrReturn.objects.filter(customer__pk__in=customers_ids).delete()
        SaleEntryLog.objects.filter(customer__pk__in=customers_ids).delete()
        OutstandingLog.objects.filter(customer__pk__in=customers_ids).delete()
        Transaction.objects.filter(customer__pk__in=customers_ids).delete()
        CustomerCoupons.objects.filter(customer__pk__in=customers_ids).delete()
        Transactionn.objects.filter(customer__pk__in=customers_ids).delete()
        CollectionPayment.objects.filter(customer__pk__in=customers_ids).delete()
        SalesmanSpendingLog.objects.filter(customer__pk__in=customers_ids).delete()
        CustomerProductReturn.objects.filter(customer__pk__in=customers_ids).delete()
        CustomerProductReplace.objects.filter(customer__pk__in=customers_ids).delete()
        CustomerProductReplace.objects.filter(customer__pk__in=customers_ids).delete()
        
        
