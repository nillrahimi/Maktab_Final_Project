from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView
from django.views.generic.edit import UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *



class Home(ListView):
    model = Branch
    template_name = 'home.html'


class AdminPanel(CreateView):
    model = Food
    template_name = 'restaurant/admin_panel.html'
    fields = '__all__'
    success_url = reverse_lazy('food_list')

class FoodList(ListView):
    model = Food
    template_name = 'restaurant/food_list.html'
    fields = '__all__'
    # success_url = reverse_lazy('Foods')
# ADD CATEGORY    
class AddCategory(CreateView):
    model = TypeCategory
    template_name = 'restaurant/add_category.html'
    fields = '__all__'

# EDIT FOOD 
class EditFood(UpdateView):
    model = Food
    template_name = 'restaurant/food_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('food_list')

class DeleteFood(DeleteView):
    model = Food 
    template_name = 'restaurant/food_delete.html'
    fields = '__all__'
    success_url = reverse_lazy('food_list')

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