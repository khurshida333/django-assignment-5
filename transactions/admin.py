from typing import Any
from django.contrib import admin
from .models import Transaction
from .views import send_transaction_email

# Register your models here.

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account','amount','balance_after_transaction','transaction_type']
