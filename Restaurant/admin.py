from django.contrib import admin
from .models import *

from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin
    
	
# @admin.register(Food)
# class FirstModelAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
# 	list_display = "__all__"
# 	readonly_fields = ('some_fields', 'date_field',)
# 	# you can override formfield, for example:

	
# 	def get_created_jalali(self, obj):
# 		return datetime2jalali(obj.created).strftime('%y/%m/%d _ %H:%M:%S')
	
# 	get_created_jalali.short_description = 'تاریخ ایجاد'
# 	get_created_jalali.admin_order_field = 'created'


admin.site.register(TypeCategory)
admin.site.register(MealCategory)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["city",'street', 'alley']
    list_display_links = ['street']
    # list_editable = []
    list_filter = ['city']
    search_fields = ['street']
    empty_value_display = '---'
    list_per_page = 5

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']
    # list_editable = []
    # list_filter = ['']
    search_fields = ['name']
    empty_value_display = '---'
    list_per_page = 5

@admin.register(Branch)
class BranchAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['name','restaurant', 'manager', 'type_category', 'city', 'created_time_jalali']
    list_display_links = ['name']
    # list_editable = []
    list_filter = ['city']
    search_fields = ['name', 'restaurant', 'manager']
    # date_hierarchy = 'created_time'
    empty_value_display = '---'
    list_per_page = 5
    def created_time_jalali(self, obj):
        return datetime2jalali(obj.created_time).strftime('%y/%m/%d _ %H:%M:%S')


@admin.register(Food)
class FoodAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['name', 'created_time_jalali']
    list_display_links = ['name']
    # list_editable = []
    list_filter = ['meal_category', 'type_category']
    search_fields = ['name', 'meal_category', 'type_category']
    # date_hierarchy = 'created_time'
    empty_value_display = '---'
    list_per_page = 5
    def created_time_jalali(self, obj):
        return datetime2jalali(obj.created_time).strftime('%y/%m/%d _ %H:%M:%S')


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['branch', 'food', 'remaining', 'price']
    list_display_links = ['branch', 'food']
    # list_editable = []
    list_filter = ['branch', 'food', 'price']
    search_fields = ['branch', 'food']
    empty_value_display = '---'
    list_per_page = 5


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ['status']
    # list_editable = ['status']
    search_fields = ['status']
    empty_value_display = '---'
    list_per_page = 5


@admin.register(OrderItem)
class OrderItemAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['order', 'number', 'created_time_jalali']
    list_display_links = ['order']
    list_editable = ['number']
    date_hierarchy = 'created_time'
    empty_value_display = '---'
    list_per_page = 5
    def created_time_jalali(self, obj):
        return datetime2jalali(obj.created_time).strftime('%y/%m/%d _ %H:%M:%S')

