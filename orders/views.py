from django.shortcuts import render
from .models import Order
from cart.cart import Cart
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from photos.models import Photo

def order_create(request):

    if request.user.is_authenticated():
            cart = Cart(request)
           # idd = User.id
            #entry = User.objects.get(pk=idd)
            idd = request.user.id
            entry = User.objects.get(pk=idd)
            for item in cart:
                #productid = Photo.id
                Order.objects.create(userid = entry, product = item['product'])
            # clear the cart
            cart.clear()
            return render(request,
                          'created.html')
    else:
        return HttpResponseRedirect('/users/login/')