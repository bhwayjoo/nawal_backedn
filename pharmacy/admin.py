from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Product, Order, OrderItem, Prescription, Address

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_admin')
    list_filter = ('is_admin', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'address', 'is_admin')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'address', 'is_admin')}),
    )

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__email')
    inlines = [OrderItemInline]

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'requires_prescription')
    list_filter = ('category', 'requires_prescription')
    search_fields = ('name', 'description')

class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'uploaded_at')
    list_filter = ('status', 'uploaded_at')
    search_fields = ('user__username', 'user__email')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Prescription, PrescriptionAdmin)
admin.site.register(Address)

