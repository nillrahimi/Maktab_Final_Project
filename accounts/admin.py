from django.contrib import admin
from .models import *


@admin.register(CustomUser)
class CustomUserInAdmin(admin.ModelAdmin): 
    model = CustomUser
    list_display = ['email','username','is_staff','is_superuser']
    list_editable = ['username']
    empty_value_display = '---'
    list_filter = ['first_name','last_name']
    search_fields = ['username', 'last_name']
    list_per_page = 5


@admin.register(Customer)
class CustomCustomer(admin.ModelAdmin):
    list_display = ["id",'email','username','first_name','last_name']
    list_display_links = ['username']
    list_editable = ['first_name','last_name']
    list_filter = ['first_name','last_name']
    search_fields = ['username', 'last_name']
    # date_hierarchy = 'created_at'
    empty_value_display = '---'
    list_per_page = 5

    def get_queryset(self, request):
        return Customer.objects.filter(is_staff= False)


@admin.register(Admin)
class CustomAdmin(admin.ModelAdmin):
    list_display = ["id",'email','username']
    list_display_links = ['username']
    # list_editable = ['']
    list_filter = ['first_name','last_name'] #status
    search_fields = ["username", "last_name"]
    empty_value_display = '---'
    list_per_page = 5

    def get_queryset(self, request):
        return Admin.objects.filter(is_superuser = True)


@admin.register(Manager)
class CustomManager(admin.ModelAdmin):
    list_display = ["id",'email','username','first_name','last_name']
    list_display_links = ['username']
    list_editable = ['first_name','last_name']
    list_filter = ['first_name','last_name']
    # search_fields = ["username", "last_name"]
    empty_value_display = '---'
    list_per_page = 5

    def get_queryset(self, request):
        return Manager.objects.filter(is_staff= True, is_superuser = False)



   



