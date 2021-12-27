from django.contrib import admin
from .models import *


admin.site.register(Address)
admin.site.register(TypeCategory)
admin.site.register(Restaurant)
admin.site.register(Branch)
admin.site.register(MealCategory)
admin.site.register(Food)
admin.site.register(Menu)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderStatus)


