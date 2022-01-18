# Generated by Django 3.2.9 on 2022-01-18 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=50)),
                ('street', models.CharField(max_length=50)),
                ('alley', models.CharField(max_length=50)),
                ('number', models.IntegerField()),
                ('is_primary', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_address', to='accounts.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('city', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('is_primary', models.BooleanField(default=False)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.manager')),
            ],
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=300, null=True)),
                ('image', models.ImageField(upload_to='media/')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MealCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remaining', models.IntegerField()),
                ('price', models.IntegerField()),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Restaurant.branch')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food_menu', to='Restaurant.food')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Restaurant.address')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_order', to='accounts.customer')),
            ],
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='ordered', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TypeCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='menu_orderitem', to='Restaurant.menu')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Restaurant.order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderstatus_order', to='Restaurant.orderstatus'),
        ),
        migrations.AddField(
            model_name='food',
            name='meal_category',
            field=models.ManyToManyField(related_name='mealcategory_food', to='Restaurant.MealCategory'),
        ),
        migrations.AddField(
            model_name='food',
            name='type_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='typecategory_food', to='Restaurant.typecategory'),
        ),
        migrations.AddField(
            model_name='branch',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restaurant_branch', to='Restaurant.restaurant'),
        ),
        migrations.AddField(
            model_name='branch',
            name='type_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Restaurant.typecategory'),
        ),
    ]
