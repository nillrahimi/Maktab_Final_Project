from django import forms
from django.forms import ModelForm
from .models import *



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
