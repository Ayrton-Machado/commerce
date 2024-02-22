from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, AuctionListing, Category
from django.contrib.auth.decorators import login_required

def index(request):
    auctions = AuctionListing.objects.all()
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        'auctions': auctions,
        'categories': categories
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        # create listing form 
        title = request.POST.get('title')
        description = request.POST.get('description')
        bidstart = request.POST.get('bidstart')
        urlImage = request.POST.get('urlImage')
        createdBy = request.user
        category_item = request.POST.get('category')
        #adicionanar categoria ao listamento
        category = Category.objects.get(categories=category_item)
        AuctionListing(title=title, description=description, bidstart=bidstart, urlImage=urlImage, createdBy=createdBy, category=category).save()
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'auctions/createlisting.html', {
        'categories': categories
    })