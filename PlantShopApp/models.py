from django.db import models
from django.contrib.auth.models import User, AbstractUser, PermissionsMixin


# Create your models here.

class Client(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=11, default="070 123 456")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"

class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Shopping cart for user {self.user.username}"

class Category(models.Model):
    family = models.CharField(max_length=50)
    light = models.CharField(max_length=50)
    water = models.CharField(max_length=50)

    def __str__(self):
        return self.family

class Plant(models.Model):
    code = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    size = models.CharField(max_length=1)
    availableQuantity = models.IntegerField()
    available = models.BooleanField(default=False)
    photo = models.ImageField(upload_to="photos/", blank=True, null=True)

    def __str__(self):
        return self.name

class PlantInShoppingCart(models.Model):
    shoppingCart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Item {self.plant.name} x {self.quantity}"

class Card(models.Model):
    cardNumber = models.CharField(max_length=16)
    expirationDate = models.CharField(max_length=5)
    cvv = models.CharField(max_length=3)
    cardHolder = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.cardNumber

class Payment(models.Model):
    code = models.AutoField(primary_key=True)
    date = models.DateField(auto_now=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    shoppingCart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, blank=True, null=True)
    deliveryAddress = models.CharField(max_length=50)
    paymentAddress = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"payment {self.code}"
