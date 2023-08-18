# Generated by Django 4.2.2 on 2023-08-11 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PlantShopApp', '0009_client_user_alter_card_owner_shoppingcart_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlantInShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='saleitem',
            name='plant',
        ),
        migrations.RemoveField(
            model_name='saleitem',
            name='sale',
        ),
        migrations.RemoveField(
            model_name='plant',
            name='shoppingCart',
        ),
        migrations.AddField(
            model_name='payment',
            name='date',
            field=models.DateField(auto_now=True),
        ),
        migrations.DeleteModel(
            name='Sale',
        ),
        migrations.DeleteModel(
            name='SaleItem',
        ),
        migrations.AddField(
            model_name='plantinshoppingcart',
            name='plant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PlantShopApp.plant'),
        ),
        migrations.AddField(
            model_name='plantinshoppingcart',
            name='shoppingCart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PlantShopApp.shoppingcart'),
        ),
    ]
