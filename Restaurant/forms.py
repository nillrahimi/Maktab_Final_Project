from django import forms
from django.forms import ModelForm
from .models import *
from accounts.models import *
from django.db.models import Q, fields


class AdminPanelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdminPanelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Food
        fields = '__all__'


class AddCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddCategoryForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = TypeCategory
        fields = '__all__'


class EditFoodForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditFoodForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Food
        fields = '__all__'


class EditProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Customer
        fields = ('username', 'last_name', 'first_name', )




class AddNewAddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddNewAddressForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Address
        fields = ('city', 'street',  'alley', 'number' , 'is_primary',)


class EditBranchInformation(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditBranchInformation, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Branch
        fields = ('name', 'type_category',  'city', 'address' , 'is_primary',)


class EditBranchMenu(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditBranchMenu, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Menu
        fields = ('food', 'remaining',  'price',)


class CreateBranchMenu(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateBranchMenu, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Menu
        fields = ('food', 'remaining',  'price',)


class OrderStatusForm(ModelForm):
    class Meta:
        model = Order
        fields = [
            'order_status',
        ]

    def __init__(self, *args, **kwargs):
        sent = OrderStatus.objects.get(status = "sent")
        delivered = OrderStatus.objects.get(status = "delivered")
        paid = OrderStatus.objects.get(status = "paid")
        super(OrderStatusForm, self).__init__(*args, **kwargs)

        if self.instance.order_status == paid:
            self.fields['order_status'].queryset = OrderStatus.objects.filter(Q(status  = "delivered")| Q(status ='sent'))
        if self.instance.order_status == sent:
            self.fields['order_status'].queryset = OrderStatus.objects.filter(status  = "delivered")
