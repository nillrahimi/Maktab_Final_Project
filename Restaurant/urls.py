from django.urls import path
from .views import *


urlpatterns = [
    path('', Home.as_view(), name='home' ),
    path('home_after', home_after_login, name='home_after'),
    path('admin_panel/', AdminPanel.as_view(), name='admin_panel'), 
    # path('manager_penal/', ManagerPanel.as_view(), name='manager_penal'), 
    # path('customer_panel/', CustomerPanel.as_view(), name='customer_panel'),
]
