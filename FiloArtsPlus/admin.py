from django.contrib import admin
from .models import Client, Drawing,Transaction

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_email', 'filled_at')
    search_fields = ('client_name', 'client_email')

@admin.register(Drawing)
class DrawingAdmin(admin.ModelAdmin):
    list_display = ('drawing_name', 'drawing_artist', 'drawing_price')
    search_fields = ('drawing_name', 'drawing_artist')
    list_filter = ('drawing_price',)
    ordering = ('-drawing_price',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'phone_number', 'amount', 'status', 'mpesa_receipt_number', 'transaction_date')
    list_filter = ('status', 'date_created', 'transaction_date')
    search_fields = ('transaction_id', 'phone_number', 'mpesa_receipt_number')

# @admin.register(User1)
# class User1Admin(admin.ModelAdmin):
#     list_display = ('user_name', 'user_email')
#     search_fields = ('user_name', 'user_email')
