from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from PlantShopApp.forms import AddToCartForm, PaymentForm
from PlantShopApp.models import *

def home(request):
    pothos = Plant.objects.filter(category__family="Pothos").all()
    calathea = Plant.objects.filter(category__family="Calathea").all()
    rarePlants = Plant.objects.filter(price__gt=1300)
    context = {"pothos": pothos, "calathea": calathea, 'rarePlants': rarePlants}
    return render(request, "home.html", context)

def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = 'Invalid username or password'
    else:
        error = None

    return render(request, 'login.html', {'error': error})


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.create_user(username=username, email=email, password=password)

        return redirect('login')

    return render(request, 'register.html')

def logoutView(request):
    logout(request)
    return redirect('home')

def profile(request):
    return render(request, "profile.html")

def payment(request):
    return render(request, "payment.html")

def plants(request):
    plants = Plant.objects.all()
    categories = Category.objects.all()
    context = {"plants": plants, "categories": categories}
    return render(request, "plants.html", context)


def singlePlant(request, code):
    plant = get_object_or_404(Plant, code=code)
    return render(request, 'singlePlant.html', {'plant': plant})

def successfulPayment(request):
    return render(request, "successfulPayment.html")

def aboutUs(request):
    return render(request, "aboutus.html")

def care(request):
    return render(request, "care.html")


@login_required
def add_to_cart(request, plant_id):
    plant = get_object_or_404(Plant, code=plant_id)

    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            shoppingCart, created = ShoppingCart.objects.get_or_create(user=request.user)
            plant, created = PlantInShoppingCart.objects.get_or_create(shoppingCart=shoppingCart, plant=plant, defaults={'quantity': quantity})
            if not created:
                plant.quantity += quantity
                plant.save()
            return redirect('shoppingCart')
    else:
        form = AddToCartForm()

    context = {
        'plant': plant,
        'form': form,
    }
    return render(request, 'shoppingCart.html', context)

def shoppingCart(request):
    if request.user.is_authenticated:
        shopping_cart_items = PlantInShoppingCart.objects.filter(shoppingCart__user=request.user)
        total_price = sum(item.quantity * item.plant.price for item in shopping_cart_items)

        context = {
            'shopping_cart_items': shopping_cart_items,
            'total': total_price
        }
        return render(request, 'shoppingCart.html', context)
    else:
        return render(request, 'shoppingCart.html')
def remove_from_cart(request, item_id):
    if request.user.is_authenticated:
        try:
            item = PlantInShoppingCart.objects.get(pk=item_id)
            if item.shoppingCart.user == request.user:
                if request.method == 'POST':
                    quantity_to_remove = int(request.POST.get('quantity', 1))
                    if 1 <= quantity_to_remove <= item.quantity:
                        if quantity_to_remove == item.quantity:
                            item.delete()
                        else:
                            item.quantity -= quantity_to_remove
                            item.save()
        except PlantInShoppingCart.DoesNotExist:
            pass
    return redirect('shoppingCart')


def search_plants(request):
    query = request.GET.get('query')

    if query:
        plants = Plant.objects.filter(Q(name__icontains=query))
    else:
        plants = Plant.objects.all()

    context = {
        'plants': plants,
    }
    return render(request, 'plants.html', context)


def checkout(request):
    user = request.user

    shopping_cart_items = PlantInShoppingCart.objects.filter(shoppingCart__user=user)
    total_price = sum(item.quantity * item.plant.price for item in shopping_cart_items)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            card_data = {
                'cardNumber': form.cleaned_data['cardNumber'],
                'expirationDate': form.cleaned_data['expirationDate'],
                'cvv': form.cleaned_data['cvv'],
                'cardHolder': request.user
            }

            # Check if a card with the same information exists
            existing_card = Card.objects.filter(
                cardNumber=card_data['cardNumber'],
                expirationDate=card_data['expirationDate'],
                cvv=card_data['cvv'],
                cardHolder=card_data['cardHolder']
            ).first()

            if existing_card:
                card = existing_card
            else:
                card = Card(**card_data)
                card.save()

            client_data = {
                'firstName': form.cleaned_data['firstName'],
                'lastName': form.cleaned_data['lastName'],
                'address': form.cleaned_data['deliveryAddress'],
                'email': form.cleaned_data['email'],
                'phone': form.cleaned_data['phone'],
                'user': request.user,
            }

            # Check if a client with the same information exists
            existing_client = Client.objects.filter(
                firstName=client_data['firstName'],
                lastName=client_data['lastName'],
                address=client_data['address'],
                email=client_data['email'],
                phone=client_data['phone'],
                user=client_data['user']
            ).first()

            if existing_client:
                client = existing_client
            else:
                client = Client(**client_data)
                client.save()

            payment_data = {
                'client': client,
                'deliveryAddress': form.cleaned_data['deliveryAddress'],
                'paymentAddress': form.cleaned_data['paymentAddress'],
                'city': form.cleaned_data['city'],
                'country': form.cleaned_data['country'],
                'card': card,
                'comment': form.cleaned_data['comment']
            }
            payment = Payment(**payment_data)
            payment.save()

            shopping_cart_items = PlantInShoppingCart.objects.filter(shoppingCart__user=user)
            shopping_cart_items.delete()

            return redirect('success')
    else:
        form = PaymentForm()

    context = {
        'form': form,
        'shopping_cart_items': shopping_cart_items,
        'total' : total_price,
    }
    return render(request, 'payment.html', context)