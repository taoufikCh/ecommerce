from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect

from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail

from addresses.forms import AddressForm
from addresses.models import Address

from billing.models import BillingProfile
from orders.models import Order
from products.models import Product
from .models import Cart

import stripe
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_Mta9z0YWMRl3mai5P6l2Nc3v00ny4Avo6o")
STRIPE_PUB_KEY =  getattr(settings, "STRIPE_PUB_KEY", 'pk_test_nM3sppFL0ed1cxzmkXCjwv3r00Yk4Bw1H9')
stripe.api_key = STRIPE_SECRET_KEY

def cart_detail_api_view(request):
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	products = [{
		"id": x.id,
		"url": x.get_absolute_url(),
		"name": x.name, 
		"price": x.price
		} 
		for x in cart_obj.products.all()] # [<object>, <objects>, <objects>]
	# products_list = []
	# for x in cart_obj.products.all():
	# 	products_list.append(
	# 			{"name": x.name, "price": x.price}
	# 		)
	cart_data = {"products": products, "subtotal": cart_obj.subtotal, "total": cart_obj.total}
	return JsonResponse(cart_data)


def cart_home(request):
	
	cart_obj, new_obj = Cart.objects.new_or_get(request)
		# products = cart_obj.products.all()
		# total = 0
		# for x in products:
		# 	total += x.price
		# print(total)
		# cart_obj.total = total
		# cart_obj.save()
	# del request.session['cart_id'] # delete
	# #request.session['cart_id'] = "12"
	# #cart_id = request.session.get("cart_id", None)
	# if cart_id is None: # and isinstance(cart_id, int):
	# 	# print('create new cart')
	# 	cart_obj =  cart_create()
	# 	request.session['cart_id'] = cart_obj.id

	# else:

	# qs =  Cart.objects.filter(id=cart_id)
	# if qs.count() == 1:
	# 	# print ('Cart ID exists')
	# 	cart_obj = qs.first()
	# 	if request.user.is_authenticated:
	# 		cart_obj.user = request.user
	# 		cart_obj.save()
	# else:
	# 	cart_obj = Cart.objects.new(user=request.user)
	# 	request.session['cart_id'] = cart_obj.id

	# print(request.session)
	# print(dir(request.session))
	# request.session.set_expiry(300) # 5 minutes
	# key = request.session.session_key
	# print(key)
	# request.session['cart_id'] = 12 # set
	# request.session['user'] = request.user.username
	return render(request, "carts/home.html", {"cart": cart_obj})


def cart_update(request):
	product_id = request.POST.get('product_id')
	if product_id is not None:
		try:
			product_obj = Product.objects.get(id=product_id)
		except Product.DoesNotExist:
			print("Show message to user, product is gone?")
			return redirect("cart:home")
		cart_obj, new_obj = Cart.objects.new_or_get(request)
		if product_obj in cart_obj.products.all():
			cart_obj.products.remove(product_obj)
			added = False
		else:
			cart_obj.products.add(product_obj) # cart_obj.products.Add(product_id)
			added = True
		request.session['cart_items'] = cart_obj.products.count()
	# cart_obj.save()
	# return redirect(product_obj.get_absolute_url())
	if request.is_ajax():
		print("ajax request")
		json_data = {
			"added": added,
			"removed": not added,
			"cartItemCount": cart_obj.products.count()
		}
		return JsonResponse(json_data, status=200) # HttpResponse
		# return JsonResponse({"message": "Error 400"}, status=400) # Django Rest Framework
	return redirect("cart:home")


def checkout_home(request):
	cart_obj, cart_created = Cart.objects.new_or_get(request)
	order_obj = None
	if cart_created or cart_obj.products.count() == 0 :
		return redirect("cart:home")

	login_form = LoginForm()
	guest_form = GuestForm()
	address_form = AddressForm()
	billing_address_id = request.session.get("billing_address_id", None)
	shipping_address_id = request.session.get("shipping_address_id", None)

	billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

	address_qs = None
	has_card = False
	if billing_profile is not None:
		if request.user.is_authenticated:
			address_qs = Address.objects.filter(billing_profile=billing_profile)
		order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
		if shipping_address_id:
			order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
			del request.session['shipping_address_id']
		if billing_address_id:
			order_obj.billing_address = Address.objects.get(id=billing_address_id)
			del request.session["billing_address_id"]
		if billing_address_id or shipping_address_id:
			order_obj.save()
		has_card = billing_profile.has_card

	if request.method == "POST":
		"check that order is done"
		is_prepared = order_obj.check_done()
		if is_prepared:
			did_charge, crg_msg = billing_profile.charge(order_obj)
			if did_charge:
				order_obj.mark_paid()
				request.session['cart_items'] = 0
				del request.session['cart_id']
				if not billing_profile.user:
					'''
					is this the bes spot?
					'''
					billing_profile.set_cards_inactive()
				return redirect("cart:success")
			else:
				print(crg_msg)
				return redirect("cart:checkout")

	context = {
	"object": order_obj,
	"billing_profile": billing_profile,
	"login_form":login_form,
	"guest_form": guest_form,
	"address_form": address_form,
	"address_qs": address_qs,
	"has_card": has_card,
	"publish_key": STRIPE_PUB_KEY,
	}
	return render(request, "carts/checkout.html", context)

def checkout_done_view(request):
	return render(request, "carts/checkout-done.html", {})