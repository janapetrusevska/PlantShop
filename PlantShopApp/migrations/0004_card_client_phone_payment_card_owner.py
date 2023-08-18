# Generated by Django 4.2.2 on 2023-06-17 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PlantShopApp', '0003_remove_category_available_plant_available'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cardNumber', models.IntegerField()),
                ('expirationDate', models.DateField()),
                ('cvv', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='client',
            name='phone',
            field=models.CharField(default='070 123 456', max_length=11),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('code', models.AutoField(primary_key=True, serialize=False)),
                ('deliveryAddress', models.CharField(max_length=50)),
                ('paymentAddress', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('comment', models.TextField(blank=True, null=True)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PlantShopApp.card')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PlantShopApp.client')),
            ],
        ),
        migrations.AddField(
            model_name='card',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PlantShopApp.client'),
        ),
    ]
