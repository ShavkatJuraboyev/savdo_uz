from django.contrib import admin
from .models import Category, Product, Order, Gallery, Certificate, News
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_uz', 'name_en', 'name_ru', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name_en',)}
    search_fields = ('name_uz', 'name_en', 'name_ru',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    list_per_page = 10
    readonly_fields = ('created_at',)  # faqat o‘qish uchun
    fieldsets = (
        ('Uzbekcha ma\'lumot', {
            'fields': ('name_uz',)  
        }),
        ('Inglizcha ma\'lumot', {
            'fields': ('name_en',)  
        }),
        ('Ruscha ma\'lumot', {
            'fields': ('name_ru',)  
        }),
        ('Maxsulot turlari', {
            'fields': ('slug',)
        }),
    )  
    def has_add_permission(self, request):
        return True 
    def has_change_permission(self, request, obj=None):
        return True 
    def has_delete_permission(self, request, obj=None):
        return True

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name_uz', 'name_en', 'name_ru', 'available', 'category', 'created_at')
    prepopulated_fields = {'slug': ('name_en',)}
    search_fields = ('name_uz',)
    list_filter = ('available', 'category')
    ordering = ('-created_at',)
    list_per_page = 10
    fieldsets = (
        ('Maxsulot haqida', {
            'fields': ('category', 'image', 'files', 'available',  )
        }),
        ('Uzbekcha ma\'lumot', {
            'fields': ('name_uz', "description_uz", 'content_uz')  
        }),
        ('Inglizcha ma\'lumot', {
            'fields': ('name_en', "description_en", 'content_en')  
        }),
        ('Ruscha ma\'lumot', {
            'fields': ('name_ru', "description_ru", 'content_ru', 'slug', )  
        }),
        
    )   
    def has_add_permission(self, request):
        return True 
    def has_change_permission(self, request, obj=None):
        return True 
    def has_delete_permission(self, request, obj=None):
        return True
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone',  'note',  'created_at')
    search_fields = ('full_name',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    list_per_page = 10
    fieldsets = (
        ('Buyurtma haqida ma\'lumotlar', {
            'fields': ('full_name', 'email', 'phone',  'note')
        }),
    )
    

admin.site.register(Gallery)
admin.site.register(Order, OrderAdmin)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Certificate)
admin.site.register(News)