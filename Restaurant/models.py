from django.db import models
import jdatetime

class TypeCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField( max_length=50)
    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField( max_length=50, unique=True)
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE, related_name="restaurant_branch")
    manager = models.ForeignKey("accounts.Manager", on_delete=models.CASCADE)
    type_category = models.ForeignKey(TypeCategory,on_delete=models.CASCADE)
    city = models.CharField( max_length=50)
    address = models.CharField( max_length=50)
    created_time = models.DateTimeField(auto_now_add=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
            if self.is_primary:
                if Branch.objects.filter(is_primary=True,manager = self.manager):
                    Branch.objects.filter(is_primary=True,manager = self.manager).update(is_primary = False)  
            
            else:
                if Branch.objects.filter(is_primary=True,manager = self.manager):
                    pass
                else:
                    first_address = Branch.objects.filter(manager = self.manager).first()
                    Branch.objects.filter(manager = first_address.manager).update(is_primary = True)  

            super(Branch, self).save(*args, **kwargs)
    # def save(self, *args, **kwargs):
    #     if self.is_primary:
    #         try:
    #             temp = Branch.objects.get(is_primary=True)
    #             if self != temp:
    #                 self.is_primary = False
    #                 self.save()
    #         except Branch.DoesNotExist:
    #             pass
    #     super(Branch, self).save(*args, **kwargs)

    @property 
    def created_at_jalali(self):
        converted = jdatetime.datetime.fromgregorian(datetime= self.created_time)
        return f'{converted.year}/{converted.month}/{converted.day} - {converted.hour}:{converted.minute}'


class MealCategory(models.Model):
    name = models.CharField( max_length=50)
    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=50)
    type_category = models.ForeignKey(TypeCategory, on_delete=models.CASCADE,related_name = "typecategory_food")
    meal_category = models.ManyToManyField(MealCategory,related_name = "mealcategory_food" )
    description = models.CharField( max_length=300,null=True,blank =True)
    image = models.ImageField(upload_to='media/')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property 
    def created_at_jalali(self):
        converted = jdatetime.datetime.fromgregorian(datetime= self.created_time)
        return f'{converted.year}/{converted.month}/{converted.day} - {converted.hour}:{converted.minute}'



class Menu(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE,related_name = "food_menu")
    remaining = models.IntegerField()
    price = models.IntegerField()


    def __str__(self):
        return f"Menu: {self.id}"



class OrderStatus(models.Model):
    # status_choices = [
    # ('ordered', 'Ordered'),
    # ('paid', 'Paid'),
    # ('sent', 'Sent'),
    # ('delivered' , 'Delivered')]
    # choices=status_choices,
    status = models.CharField(max_length=50, default='ordered',)

    def __str__(self):
        return self.status



class OrderItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.DO_NOTHING, related_name='menu_orderitem')
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    number = models.IntegerField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order: {self.id} From: {self.order}"

    @property
    def get_total_price(self):
        menu_price = Menu.objects.filter(id=self.menu.id).values_list("price")[0][0]

        return menu_price * self.number

    @property 
    def created_at_jalali(self):
        converted = jdatetime.datetime.fromgregorian(datetime= self.created_time)
        return f'{converted.year}/{converted.month}/{converted.day} - {converted.hour}:{converted.minute}'
    

class Order(models.Model):
    order_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, related_name='orderstatus_order')
    customer = models.ForeignKey("accounts.Customer", on_delete=models.CASCADE,related_name = "customer_order")
    created_time = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey('Address', on_delete=models.DO_NOTHING, null= True, blank=True)
    
    def __str__(self):
        return '{} {}'.format(self.customer ,self.order_status)

    @property
    def get_cart_total(self):
        orderitems = OrderItem.objects.filter(order=self.id)
        if orderitems:
            return sum([item.get_total_price for item in orderitems]) 
        else:
            return 0

    @property 
    def created_at_jalali(self):
        converted = jdatetime.datetime.fromgregorian(datetime= self.created_time)
        return f'{converted.year}/{converted.month}/{converted.day} - {converted.hour}:{converted.minute}'


        

class Address(models.Model):
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    alley =  models.CharField(max_length=50)
    number = models.IntegerField()
    customer = models.ForeignKey('accounts.Customer',on_delete=models.CASCADE,  related_name='customer_address')
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return '{} {}'.format(self.street ,self.customer)

    def save(self, *args, **kwargs):
            if self.is_primary:
                if Address.objects.filter(is_primary=True,customer = self.customer):
                    Address.objects.filter(is_primary=True,customer = self.customer).update(is_primary = False)  
            
            else:
                if Address.objects.filter(is_primary=True,customer = self.customer):
                    pass
                else:
                    first_address =  Address.objects.filter(customer = self.customer).first()
                    Address.objects.filter(customer = first_address.customer).update(is_primary = True)  

            super(Address, self).save(*args, **kwargs)
    # def save(self, *args, **kwargs):
    #     if self.is_primary:
    #         try:
    #             temp = Address.objects.get(is_primary=True)
    #             if self != temp:
    #                 self.is_primary = False
    #                 self.save()
    #         except Address.DoesNotExist:
    #             pass
    #     super(Address, self).save(*args, **kwargs)




