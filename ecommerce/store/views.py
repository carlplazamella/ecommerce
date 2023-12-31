from django.shortcuts import render
from django.http import JsonResponse
import json


from .models import *

def store(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems =  order.get_cart_items	
	else: 
		item = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']
	
	products = Product.objects.all()
	context = {'products': products, 'cartItems': cartItems}
	return render(request, 'store/store.html', context)

def cart(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else: 
		item = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
		cartItems = order['get_cart_items']


	context = {'item': items, 'order':order, 'cartItems': cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else: 
		item = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}

	context = {'item': items, 'order':order}	
	return render(request, 'store/checkout.html', context, 'cartItems':cartItems)

def updateItem(request):
	data = json.loads(request.data)
	productId = data['productId']
	action = data['action']

	print('Action:', action)
	print('productId:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	OrderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		OrderItem.quantity = (OrderItem.quantity + 1)
	elif action == 'remove':
		OrderItem.quantity = (OrderItem.quantity - 1)

	OrderItem.save()

	if OrderItem.quantity <= 0:
		OrderItem.delete()

		

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
		print('Data:', request.body)
		return JsonResponse('Payment Complete!', safe=False)


	