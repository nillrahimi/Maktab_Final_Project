from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Home.as_view(), name='home' ),
    path('home_after/', home_after_login, name='home_after'),
    path('admin_panel/', AdminPanel.as_view(), name='admin_panel'), 
    path('admin_panel/add_category',AddCategory.as_view(), name = 'add_category'),
    path('admin_panel/food_list/edit_food/<int:pk>/',EditFood.as_view(), name = 'edit_food'),
    path('admin_panel/food_list/delete_food/<int:pk>/',DeleteFood.as_view(), name = 'delete_food'),
    path('menu_list/<int:pk>/', MenuList.as_view(), name='menu_list'),
    path('admin_panel/food_list/',  FoodList.as_view(), name='food_list'),
   
    # path('manager_penal/', ManagerPanel.as_view(), name='manager_penal'), 
    # path('customer_panel/', CustomerPanel.as_view(), name='customer_panel'),
]



urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)