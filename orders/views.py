from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .cart import Cart
from home.models import Product
from .forms import CartAddForm, CouponApplyForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Order, OrderItem, Coupon
from django.conf import settings
import json
import requests
import datetime
from django.http import HttpResponse
from django.contrib import messages

class CartView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, "orders/cart.html", {"cart": cart})


class CartAddView(PermissionRequiredMixin, View):
    permission_required = ('orders.add_order',)
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data["quantity"])
        return redirect("orders:cart")


class CartRemove(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect("orders:cart")


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            print(item)
            OrderItem.objects.create(
                order=order,
                product=item["product_name"],
                price=item["price"],
                quantity=item["quantity"],
            )
        cart.clear()
        return redirect("orders:order_detail", order.id)


class OrderDetailView(LoginRequiredMixin, View):
    form_class = CouponApplyForm
    
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, "orders/order.html", {"order": order, 'form': self.form_class})


ZP_API_REQUEST = f"https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://sandbox.zarinpal.com/pg/StartPay/"


class OrderPayView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        request.session['order_pay'] = {
            'order_id': order.id,
        }
        req_data = {
            "MerchantID": settings.MERCHANT,
            "Amount": order.get_total_price(),
            "Description": "Transaction details...",
            "CallbackURL": "http://127.0.0.1:8000/orders/verify/",
            "metadata": {"mobile": request.user.phone_number, "email": request.user.email}
        }
        req_header = {"accept": "application/json",
                        "content-type": "application/json'"}
        req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
            req_data), headers=req_header)
        authority = req.json()['Authority']
        if 'errors' not in req.json().keys():
            return redirect(ZP_API_STARTPAY.format(authority=authority))
        else:
            print(req.json()) 
            return HttpResponse(f"An error happend{req.json()}")
        # if len(req.json()['errors']) == 0:
        #     return redirect(ZP_API_STARTPAY.format(authority=authority))
        # else:
        #     e_code = req.json()['errors']['code']
        #     e_message = req.json()['errors']['message']
        #     return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


class OrderVerifyView(LoginRequiredMixin, View):
    def get(self, request):
        
        order_id = request.session['order_pay']['order_id']
        order = Order.objects.get(id=int(order_id))
        
        t_status = request.GET.get('Status')
        t_authority = request.GET['Authority']
        
        if request.GET.get('Status') == 'OK':
            req_header = {"accept": "application/json",
                          "content-type": "application/json'"}
            req_data = {"merchant_id": settings.MERCHANT,
                        "amount": order.get_total_price(), # with this value zarinpal checks amount of money.
                        "authority": t_authority
                        }
            # for checking data
            req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
            if 'errors' not in req.json().keys():
                t_status = req.json()['code']
                if t_status == 100:
                    #*** save codindition of paying.
                    order.paid = True
                    order.save()
                    #*** we must save ref_id in a table.
                    return HttpResponse('Transaction success.\nRefID: ' + str(req.json(['ref_id'])))
                # Repetitivre transaction and will not doing again(code 101).
                elif t_status == 101:
                    return HttpResponse('Transaction submitted : ' + str(req.json()))
                else:
                    return HttpResponse('Transaction failed.\nStatus: ' + str(req.json()))
            else:
                print(req.json()) 
                return HttpResponse(f"An error happend{req.json()}")
        else:
            return HttpResponse('Transaction failed or canceled by user')

class CouponApplyView(LoginRequiredMixin, View):
    form_class = CouponApplyForm
    def post(self, request, order_id):
        now = datetime.datetime.now()
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__exact=code, valid_from__lte=now, 
                                            valid_to__gte=now, active=True)
            except Coupon.DoesNotExist:
                messages.error(request, 'coupon does not extist.', 'danger')
                return redirect('orders:order_detail', order_id)
                
            order = Order.objects.get(id=order_id)
            order.discount = coupon.discount
            order.save()
        return redirect('orders:order_detail', order_id)
            

        