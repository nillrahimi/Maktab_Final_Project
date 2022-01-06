from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Sum
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView
from django.views.generic.edit import UpdateView, DeleteView
from .models import *
from .forms import *
from accounts.models import Customer
from django.db.models import Q
# from django.utils.decorators import method_decorator
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth import REDIRECT_FIELD_NAME
# from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin

def superuser_required():
    def wrapper(wrapped):
        class WrappedClass(UserPassesTestMixin, wrapped):
            def test_func(self):
                return self.request.user.is_superuser

        return WrappedClass
    return wrapper



#JALALI
from datetime import date, datetime
from distutils.version import StrictVersion
from django.conf import settings

from jalali_date import date2jalali, datetime2jalali
from django.template import Library
register = Library()
DEFAULTS = settings.JALALI_DATE_DEFAULTS
def my_view(request):
	jalali_join = datetime2jalali(request.user.date_joined).strftime('%y/%m/%d _ %H:%M:%S')

@register.simple_tag
def jalali_now(strftime=None):
    strftime = strftime if strftime else DEFAULTS['Strftime']['datetime']
    return datetime2jalali(datetime.now()).strftime(strftime)


#HOME PAGE
class Home(ListView):
    model = Branch
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        sold_foods = Food.objects.filter(Q(food_menu__menu_orderitem__order__order_status__status__contains='delivered')|Q(food_menu__menu_orderitem__order__order_status__status__contains='sent')|Q(food_menu__menu_orderitem__order__order_status__status__contains='paid'))
        most_sold_foods = sold_foods.annotate(final=Sum('food_menu__menu_orderitem__number')).order_by('final')[:10]
        
        sold_branches = Branch.objects.filter(Q(menu__menu_orderitem__order__order_status__status__contains='delivered')|Q(menu__menu_orderitem__order__order_status__status__contains='sent')|Q(menu__menu_orderitem__order__order_status__status__contains='paid'))
        most_sold_branches = sold_branches.annotate(final=Sum('menu__menu_orderitem__number')).order_by('final')[:10]
           
        data = super().get_context_data(**kwargs)
        data['most_sold_foods'] = most_sold_foods
        data['most_sold_branches'] = most_sold_branches
        return data






#Handling
def food(request, pk):
    food = Food.objects.get(id=pk)

    if request.method == 'POST':
        food = Food.objects.get(id=pk)
        #Get user account information
        try:
            customer = request.user.customer	
        except:
            device = request.COOKIES['device']
            customer, created = Food.objects.get_or_create(device=device)

        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, food=food)
        orderItem.quantity=request.POST['number']
        orderItem.save()

        return redirect('cart')

    context = {'food':food}
    return render(request, 'store/product.html', context)

def cart(request):
    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    context = {'order':order}
    return render(request, 'store/cart.html', context)




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
        return render(request, 'manager_panel.html')

    elif not(request.user.is_staff) and not(request.user.is_superuser):
        return render(request, 'manager_panel.html')

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









