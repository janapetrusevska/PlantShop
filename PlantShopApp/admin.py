from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from PlantShopApp.models import *


# Register your models here.
# To log in here are some created users
# Username anasatsija.velovska password: Password123#
# Username petar.petrovski11 password: Password123#
# Username admin password: admin

class ClientAdmin(admin.ModelAdmin):
    list_display = ("firstName", "lastName", "email")


admin.site.register(Client, ClientAdmin)

class PlantInCategory(admin.TabularInline):
    model = Plant
    extra = 0

class CategoryAdmin(admin.ModelAdmin):
    inlines = [PlantInCategory, ]
    list_display = ("family", "light", "water")

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


admin.site.register(Category, CategoryAdmin)

class PlantAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "category", "price", "availableQuantity", "available")

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Plant, PlantAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ("code", "deliveryAddress", "city", "comment")

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


admin.site.register(Payment, PaymentAdmin)

class PaymentsInCard(admin.TabularInline):
    model = Payment
    extra = 0

class CardAdmin(admin.ModelAdmin):
    list_display = ("cardNumber", "cardHolder")
    inlines = [PaymentsInCard]

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


admin.site.register(Card, CardAdmin)

class PlantInShoppingCartInline(admin.TabularInline):
    model = PlantInShoppingCart
    extra = 1

class ShoppingCartAdmin(admin.ModelAdmin):
    inlines = [PlantInShoppingCartInline]

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


admin.site.register(ShoppingCart, ShoppingCartAdmin)