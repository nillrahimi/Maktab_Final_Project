from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *



class Home(ListView):
    model = Branch
    template_name = 'home.html'

class AdminPanel(CreateView):
    model = Food
    template_name = 'Restaurant\admin_panel.html'
    fields = '__all__'
    # success_url = reverse_lazy('Foods')

@login_required
def home_after_login(request):
    if request.user.is_superuser :
        return redirect('admin_penal.html')

    elif request.user.is_staff and not(request.user.is_superuser):
        return redirect('manager_penal.html')

    elif not(request.user.is_staff) and not(request.user.is_superuser):
        return redirect('manager_penal.html')