from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView
from django.views.generic.edit import UpdateView, DeleteView
from .models import *
from .forms import *
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


class Home(ListView):
    model = Branch
    template_name = 'home.html'

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









