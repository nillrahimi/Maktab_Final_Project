from django import template
from django.contrib.auth.decorators import login_required
from django.db import reset_queries
from django.db.models.aggregates import Sum
from django.db.models import Q, fields
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView
from django.views.generic.edit import UpdateView, DeleteView
from .models import *
from .forms import *
from .decorators import *
from accounts.models import Customer
from datetime import date, datetime
from django.conf import settings
from jalali_date import date2jalali, datetime2jalali
from django.template import Library
from django.http import HttpResponse
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
import json


#JALALI
register = Library()
DEFAULTS = settings.JALALI_DATE_DEFAULTS
def my_view(request):
	jalali_join = datetime2jalali(request.user.date_joined).strftime('%y/%m/%d _ %H:%M:%S')

@register.simple_tag
def jalali_now(strftime=None):
    strftime = strftime if strftime else DEFAULTS['Strftime']['datetime']
    return datetime2jalali(datetime.now()).strftime(strftime)


#HOME PAGE______________________________________________________________________________________________________________________
class Home(ListView):
    model = Branch
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        sold_foods = Food.objects.filter(Q(food_menu__menu_orderitem__order__order_status__status__contains='delivered')|Q(food_menu__menu_orderitem__order__order_status__status__contains='sent')|Q(food_menu__menu_orderitem__order__order_status__status__contains='paid'))
        most_sold_foods = sold_foods.annotate(final=Sum('food_menu__menu_orderitem__number')).order_by('-final')[:10]
        
        sold_branches = Branch.objects.filter(Q(menu__menu_orderitem__order__order_status__status__contains='delivered')|Q(menu__menu_orderitem__order__order_status__status__contains='sent')|Q(menu__menu_orderitem__order__order_status__status__contains='paid'))
        most_sold_branches = sold_branches.annotate(final=Sum('menu__menu_orderitem__number')).order_by('final')[:10]
           
        data = super().get_context_data(**kwargs)
        data['most_sold_foods'] = most_sold_foods
        data['most_sold_branches'] = most_sold_branches
        return data


    def post(self, request):
        if request.method == 'POST'  and request.is_ajax():
            text = request.POST.get('search_input')
            print(text)
            if text :
                branch = Branch.objects.filter(name__contains=text)
                food = Food.objects.filter(name__contains=text)
                branches ={}
                foods ={}
                if branch:
                    serializer_branch = BranchSerializer(branch,many=True,context={'request': request})
                    branches = serializer_branch.data    
                
                if food:
                    serializer_food = FoodSerializer(food,many=True,context={'request': request})
                    foods = serializer_food.data
                
                return Response({"branches":branches , "foods":foods})
                
            else:
                Response({"branches":[] , "foods":[],"msg":"does not match"})
              
        return render(request,'home.html')   




#Handling Card__________________________________________________________________________________________________________
def items(request, pk):
    menu = Menu.objects.get(id = pk)
    chosen_branch = menu.branch
    chosen_food = menu.food
    existed_branch = ''
    existed_orderitem=''
    if request.method == "POST":
        menu = Menu.objects.get(id = pk)
        chosen_branch = menu.branch
        if request.user.is_authenticated :
            customer = request.user
        else:    
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)
        
        status = OrderStatus.objects.get(status = "ordered")
        orders = Order.objects.get(Q(customer=customer)& Q(order_status=status))
        
        if orders:
            existed_orderitem = OrderItem.objects.filter(order=orders).last()

        if existed_orderitem :
            existed_food = Food.objects.filter(food_menu__menu_orderitem=existed_orderitem)
            existed_branch = Branch.objects.get(menu__menu_orderitem =existed_orderitem)

            if chosen_food in existed_food:
                context = {'food':menu, 'message':"this item already exist"}
                return render(request,'restaurant/menu_to_card.html',context)

        if existed_branch and not chosen_branch.name == existed_branch.name:
            #if not selected_branch.name == existed_branch.name:
            context = {'food':menu, 'message':"Please either Choose from One Branch Or Make Your Card Empty First"}
            return render(request,'restaurant/menu_to_card.html',context)
        
        else:
            if menu.remaining >= int(request.POST['number']) :
                status = OrderStatus.objects.get(status = "ordered")
                order, created = Order.objects.get_or_create(customer = customer, order_status =status)
                
                orderItem, created = OrderItem.objects.get_or_create(order=order, number=1 , menu=menu)
                # orderItem.menu_orderitem.get_or_create( )
                orderItem.number = request.POST['number']
                orderItem.save()
                return redirect('cart')
            else:
                context = {'food':menu, 'message':'This Branch Has Not Enough Foods'}
                return(request,'restaurant/menu_to_card.html',context)    
    context = {'food':menu}
    return render(request,'restaurant/menu_to_card.html', context)


def cart(request):
    if request.method == "POST":
        customer_address = request.POST.get("customer_address")
        pk,city,street,number =customer_address.split("_")

        choosen_address = Address.objects.get(pk = pk)

        customer = request.user
        status = OrderStatus.objects.get(status = "ordered")
        new_status = OrderStatus.objects.get(status = "complete")
        order= Order.objects.filter(customer=customer, order_status =status).update(order_status=new_status)
        msg = "successfull"
        return render(request,'restaurant/cart.html',{"msg":msg})

    addresses=''

        # device = request.COOKIES['device']
        # status = OrderStatus.objects.get(order_status = "ordered")
        
    # if request.user.is_authenticated:
        # customer = Customer.objects.get(device=device, username = device)
        # if customer:    
        #     order = Order.objects.get(customer=customer, order_status =status)
        #     if order :
        #         order_items_device = OrderItem.objects.filter(order= order.id)
        #         if order_items_device:
        #             branch_order_item_device= Branch.objects.get(menu_menu_orderitem_order = order_items_device.last().order)
        #             print(branch_order_item_device)

    if request.user.is_authenticated :
        addresses = Address.objects.filter(customer = request.user)
        customer = request.user
        status = OrderStatus.objects.get(status="ordered")
        order, created = Order.objects.get_or_create(customer=customer, order_status =status)

        device = request.COOKIES['device']
        customer_device = Customer.objects.filter(device=device).last()
        
        if customer_device:
            order_device = Order.objects.filter(customer=customer_device, order_status =status).last()
            if order_device :
                order_items_device = OrderItem.objects.filter(order = order_device.id)
                if order_items_device:
                    Order.objects.filter(id = order.id).delete()
                    Order.objects.filter(id = order_device.id).update(customer = customer)
                    Customer.objects.filter(id = customer_device.id).delete()
                    order = Order.objects.filter(customer = customer , order_status = status).last()
    
    else:  
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
        status = OrderStatus.objects.get(status="ordered")
        order, created = Order.objects.get(customer=customer, order_status =status)

    context = {'order':order, "addresses":addresses}
    return render(request, 'restaurant/cart.html', context)








#______________________________________________________________________________________________
class DeleteOrderedItem(DeleteView):
    model = OrderItem
    template_name = 'restaurant/delete_ordered_item.html'
    success_url = reverse_lazy('cart')

class EditOrderedItem(UpdateView):
    model = OrderItem
    template_name = 'restaurant/edit_ordered_item.html'
    success_url = reverse_lazy('cart')
    fields = ('number',)


#LIST of MENUES
class MenuList(ListView):
    model = Menu
    template_name = 'restaurant/menu_list.html'
    def get_queryset(self):
        return Menu.objects.filter(branch = self.kwargs['pk'])




@login_required
def home_after_login(request):
    if request.user.is_superuser :
        return redirect(reverse('admin_panel'))

    elif request.user.is_staff and not(request.user.is_superuser):
        return redirect(reverse('manager_panel'))

    elif not(request.user.is_staff) and not(request.user.is_superuser):
        return redirect(reverse('customer_panel'))

@superuser_required()
class AdminPanel(CreateView):
    model = Food
    form_class = AdminPanelForm
    template_name = 'restaurant/admin_panel.html'
    # fields = '__all__'
    success_url = reverse_lazy('food_list')

@superuser_required()
class FoodList(ListView):
    model = Food
    template_name = 'restaurant/food_list.html'
    fields = '__all__'
    # success_url = reverse_lazy('Food_list')

# EDIT FOOD 
@superuser_required()
class EditFood(UpdateView):
    model = Food
    template_name = 'restaurant/food_edit.html'
    form_class = EditFoodForm
    success_url = reverse_lazy('food_list')

# DELETE FOOD
@superuser_required()
class DeleteFood(DeleteView):
    model = Food 
    template_name = 'restaurant/food_delete.html'
    fields = '__all__'
    success_url = reverse_lazy('food_list')

# ADD CATEGORY   
@superuser_required()
class AddCategory(CreateView):
    model = TypeCategory
    template_name = 'restaurant/add_category.html'
    form_class = AddCategoryForm
    success_url = reverse_lazy('admin_panel')


#CUSTOMER PANEL________________________________________________________________________________
#Customer Panel: list of orderitems
@customer_required()
class CustomerPanel(ListView):
    model = OrderItem
    template_name = 'restaurant/customer/customer_panel.html'


#Customer Panel: Edit Profile
@customer_required()
class CustomerEditProfile(UpdateView):
    model = Customer
    form_class = EditProfileForm
    template_name = 'restaurant/customer/edit_profile.html'
    success_url = reverse_lazy('customer_panel')


@customer_required()
class CustomerAddAddress(CreateView):
    model = Address
    template_name = 'restaurant/customer/add_address.html'
    form_class = AddNewAddressForm
    success_url = reverse_lazy('customer_panel')


#ManagerPanel______________________________________________________________________________________
@manager_required()
class ManagerPanel(TemplateView):
    template_name = 'restaurant/manager/manager_panel.html'
    






#Search Bar__________________________________________________________________

# def autocompleteModel(request):
#     if request.is_ajax():
#         q = request.GET.get('term', '').capitalize()
#         search_qs = Food.objects.filter(name__startswith=q)
#         results = []
#         print (q)
#         for r in search_qs:
#             results.append(r.FIELD)
#         data = json.dumps(results)
#     else:
#         data = 'fail'
#     mimetype = 'application/json'
#     return HttpResponse(data, mimetype)








#Registerations_________________________________________________________________________________________________________________________

class SignupBase(TemplateView):
    template_name = "account/signup_base.html"

#Manager_____________________________________________________
def signup_manager (request):
    category_list = TypeCategory.objects.all()
    restaurant_list = Restaurant.objects.all()
    

    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        branch_name = request.POST.get("name")
        city = request.POST.get("city")
        address = request.POST.get("address")
        branch_type_category = request.POST.get("branch_type_category")
        restaurant = request.POST.get("restaurant")
        description = request.POST.get("description")
        is_primary = request.POST.get("is_primary")
        branch_object = TypeCategory.objects.get(name = branch_type_category)
        restaurant_object = Restaurant.objects.get( name = restaurant)
        if is_primary == "on":
            is_primary=True
        else :
            is_primary = False    
        
        manager = Manager(email = email , username = username, password = password1)
        manager.set_password(password1)
        manager.save()
        
        branch = Branch.objects.create(name = branch_name , city = city , address = address,
          restaurant = restaurant_object, manager = manager , type_category = branch_object , is_primary = is_primary)

        return redirect('account_login')

    return render(request,"account/signup_manager.html",{"categories": category_list, "restaurants":restaurant_list})

#Admin________________________________________________________

def signup_admin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        admin = Admin(email = email , username = username, password = password1)
        admin.set_password(password1)
        admin.save()
        return redirect('account_login')

    return render(request,"account/signup_admin.html")

#Customer_______________________________________________________    

def signup_customer(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        city = request.POST.get("city")
        street = request.POST.get("street")
        number = request.POST.get("number")
        is_primary = request.POST.get("is_primary")
        customer = Customer(email = email , username = username, password = password1)
        customer.set_password(password1)
        customer.save()
        address = Address.objects.create(city = city , street = street ,number = number, is_primary = True)
        address.customer.add(customer)
        return redirect('account_login')

    return render(request,"account/signup_customer.html")
