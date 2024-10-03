import datetime
from django.core.management.base import BaseCommand
from accounts.models import CustomUser, Customers
from client_management.models import CustodyCustom, CustomerOutstanding, CustomerOutstandingReport, Vacation
from customer_care.models import CouponPurchaseModel, CustodyPullOutModel, CustomerComplaint, DiffBottlesModel, OtherRequirementModel
from invoice_management.models import Invoice
from order.models import ChangeOrReturn, Customer_Order
from sales_management.models import CollectionPayment, CustomerCoupons, OutstandingLog, SaleEntryLog, SalesmanSpendingLog, Transaction, Transactionn
from van_management.models import CustomerProductReplace, CustomerProductReturn

class Command(BaseCommand):
    help = 'Generate usernames and passwords for customers based on their name and mobile number'

    def handle(self, *args, **kwargs):
        # customers = Customers.objects.filter(routes__route_name="S-02")
        # for customer in customers:
        #     if customer.user_id:
        #         CustomUser.objects.filter(pk=customer.user_id.pk).delete()
        # customers.delete()
        
        outstanding_in = CustomerOutstanding.objects.filter(created_date__date__lte=datetime.datetime.strptime("2024-08-30", '%Y-%m-%d').date())
        Invoice.objects.filter(created_date__date__lte=datetime.datetime.strptime("2024-08-30", '%Y-%m-%d').date()).delete()
        outstanding_in.delete()
        # CustomerOutstandingReport.objects.filter(created_date__date__lte=datetime.datetime.strptime("2024-08-30", '%Y-%m-%d').date()).delete()
        CollectionPayment.objects.filter(created_date__date__lte=datetime.datetime.strptime("2024-08-30", '%Y-%m-%d').date()).delete()
        
        # Invoice.objects.filter(customer__routes__route_name="S-02").delete()
        # CustomerOutstanding.objects.filter(customer__routes__route_name="S-02").delete()
        # CustomerOutstandingReport.objects.filter(customer__routes__route_name="S-02").delete()
        # CustodyCustom.objects.filter(customer__routes__route_name="S-02").delete()
        # Vacation.objects.filter(customer__routes__route_name="S-02").delete()
        # DiffBottlesModel.objects.filter(customer__routes__route_name="S-02").delete()
        # OtherRequirementModel.objects.filter(customer__routes__route_name="S-02").delete()
        # CouponPurchaseModel.objects.filter(customer__routes__route_name="S-02").delete()
        # CustodyPullOutModel.objects.filter(customer__routes__route_name="S-02").delete()
        # CustomerComplaint.objects.filter(customer__routes__route_name="S-02").delete()
        # Customer_Order.objects.filter(customer_id__routes__route_name="S-02").delete()
        # # ChangeOrReturn.objects.filter(customer__routes__route_name="S-02").delete()
        # SaleEntryLog.objects.filter(customer__routes__route_name="S-02").delete()
        # OutstandingLog.objects.filter(customer__routes__route_name="S-02").delete()
        # Transaction.objects.filter(customer__routes__route_name="S-02").delete()
        # CustomerCoupons.objects.filter(customer__routes__route_name="S-02").delete()
        # Transactionn.objects.filter(customer__routes__route_name="S-02").delete()
        # CollectionPayment.objects.filter(customer__routes__route_name="S-02").delete()
        # SalesmanSpendingLog.objects.filter(customer__routes__route_name="S-02").delete()
        # CustomerProductReturn.objects.filter(customer__routes__route_name="S-02").delete()
        # CustomerProductReplace.objects.filter(customer__routes__route_name="S-02").delete()
        # CustomerProductReplace.objects.filter(customer__routes__route_name="S-02").delete()
        
        
