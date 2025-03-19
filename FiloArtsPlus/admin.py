from django.contrib import admin
from .models import Client, Drawing,Transaction, Blog, Comment

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


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('filled_at', 'description_preview')
    ordering = ('-filled_at',)
    inlines = [CommentInline]  # Display comments inside the Blog admin panel

    def description_preview(self, obj):
        return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description
    description_preview.short_description = "Description"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'name', 'text_preview')

    def text_preview(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
    text_preview.short_description = "Comment Text"

# @admin.register(User1)
# class User1Admin(admin.ModelAdmin):
#     list_display = ('user_name', 'user_email')
#     search_fields = ('user_name', 'user_email')
