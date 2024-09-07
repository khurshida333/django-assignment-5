from django.urls import path
from .views import DepositMoneyView, TransactionReportView,BorrowBook,BorrowReportView,ReturnBook


app_name = 'transactions'

urlpatterns = [
    path("deposit/", DepositMoneyView.as_view(), name="deposit_money"),
    path("borrow/<int:id>/", BorrowBook, name="borrow_books"),
    path("return/<int:id>/", ReturnBook, name="return_books"),
    path("report/", TransactionReportView.as_view(), name="transaction_report"),
    path("borrow-report/", BorrowReportView.as_view(), name="borrow_report"),


]