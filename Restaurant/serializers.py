from rest_framework import serializers
from .models import *


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'name']

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id', 'name'] 

class MenuSerializer(serializers.ModelSerializer):
    food = FoodSerializer
    class Meta:
        model = Menu
        fields = ['food','branch'] 
