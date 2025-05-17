from django.contrib import admin
from .models import Category, Product, Order, OrderItem
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    list_per_page = 10
    list_editable = ('description',)
    readonly_fields = ('created_at',)  # faqat o‘qish uchun
    fieldsets = (
        ('Maxsulot turlari', {
            'fields': ('name', 'slug', 'description', 'image')
        }),
        ('Qo\'shimcha ma\'lumotlar', {
            'fields': ()  # bu yer bo‘sh qolsa ham bo‘ladi yoki o‘chirib tashlasa ham bo‘ladi
        }),
    )  
    def has_add_permission(self, request):
        return True 
    def has_change_permission(self, request, obj=None):
        return True 
    def has_delete_permission(self, request, obj=None):
        return True

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description', 'ingredients', 'price', 'discount_price', 'stock', 'available', 'category', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_filter = ('available', 'category')
    ordering = ('-created_at',)
    list_per_page = 10
    list_editable = ('price', 'stock')
    fieldsets = (
        ('Maxsulot haqida', {
            'fields': ('name', 'slug', 'description', 'ingredients', 'price', 'discount_price', 'stock', 'available', 'category', 'image')
        }),
    )   
    def has_add_permission(self, request):
        return True 
    def has_change_permission(self, request, obj=None):
        return True 
    def has_delete_permission(self, request, obj=None):
        return True
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'city', 'district', 'street', 'house_number', 'apartment_number', 'address', 'note', 'total_price', 'created_at')
    search_fields = ('full_name',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    list_per_page = 10
    fieldsets = (
        ('Buyurtma haqida ma\'lumotlar', {
            'fields': ('full_name', 'email', 'phone', 'city', 'district', 'street', 'house_number', 'apartment_number', 'address', 'note')
        }),
        ('Jami narx va vaqtlar', {
            'fields': ('total_price',)
        }),
    )  
    def has_add_permission(self, request):
        return True 
    def has_change_permission(self, request, obj=None):
        return True 
    def has_delete_permission(self, request, obj=None):
        return True
    
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__full_name',)
    list_filter = ('order',)
    ordering = ('-order__created_at',)
    list_per_page = 10
    fieldsets = (
        ('Buyurtma haqida ma\'lumotlar', {
            'fields': ('order', 'product', 'quantity', 'price')
        }),
    )  
    def has_add_permission(self, request):
        return True 
    def has_change_permission(self, request, obj=None):
        return True 
    def has_delete_permission(self, request, obj=None):
        return True
    
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
