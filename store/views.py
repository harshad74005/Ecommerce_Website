from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.views import View
from django.db.models import Q
from django.http import JsonResponse
import random
from django.core.mail import send_mail

from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.cart import Cart
from .models.order import OrderDetail
from datetime import datetime


# ================= HOME =====================
def home(request):
    totalitem = 0
    name = None

    if not request.session.has_key('phone'):
        return redirect('login')

    phone = request.session['phone']
    totalitem = Cart.objects.filter(phone=phone).count()

    try:
        customer = Customer.objects.get(phno=phone)
        name = customer.name
    except Customer.DoesNotExist:
        del request.session["phone"]
        return redirect('login')

    categories = Category.get_all_categories()
    categoryId = request.GET.get('category')
    search_query = request.GET.get('query')

    products = Product.objects.all()

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    elif categoryId:
        products = Product.get_all_product_by_category_id(categoryId)
    else:
        products = Product.get_all_products()

    data = {
        'name': name,
        'products': products,
        'categories': categories,
        'totalitem': totalitem
    }

    return render(request, 'home.html', data)


# ================= SIGNUP =====================
class signup(View):
    def get(self, request):
        if 'is_otp_sent' in request.session:
            del request.session['is_otp_sent']
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        name = postData.get('name')
        phone = postData.get('phone')
        email = postData.get('email')

        error_message = None
        value = {'phone': phone, 'name': name, 'email': email}

        customer = Customer(name=name, phno=phone, email=email)

        if not name or not phone or not email:
            error_message = 'All fields are required.'
        elif len(phone) < 10:
            error_message = 'Phone number must be 10 digits.'
        elif customer.isExists():
            error_message = 'Mobile Number or Email Already Exists.'

        if not error_message:
            customer.register()
            messages.success(request, "Congratulations! Registration Successful. Please log in.")
            return redirect('login')
        else:
            data = {'error': error_message, 'value': value}
            return render(request, 'signup.html', data)


# ================= LOGIN with OTP =====================
class Login(View):
    def get(self, request):
        if 'is_otp_sent' in request.session:
            del request.session['is_otp_sent']
        return render(request, 'login.html')

    def post(self, request):
        postData = request.POST

        if request.session.get('is_otp_sent') and 'otp_input' in postData:

            user_otp = postData.get('otp_input')
            session_otp = request.session.get('login_otp')

            if user_otp == session_otp:

                phone_to_login = request.session['temp_phone']

                del request.session['is_otp_sent']
                del request.session['login_otp']
                del request.session['temp_phone']

                request.session['phone'] = phone_to_login
                messages.success(request, "Login successful!")
                return redirect('homepage')

            else:
                error_message = 'Wrong OTP entered. Please try again.'
                return render(request, 'login.html', {'error': error_message, 'is_otp_sent': True})

        else:
            user_id = postData.get('user_id')
            error_message = None

            customer = Customer.objects.filter(
                Q(phno=user_id) | Q(email=user_id)
            ).first()

            if not customer:
                error_message = "Account not found. Please check your number/email or signup."

            if not error_message:
                otp = str(random.randint(100000, 999999))

                request.session['login_otp'] = otp
                request.session['temp_phone'] = customer.phno
                request.session['is_otp_sent'] = True

                try:
                    send_mail(
                        'SmartGrocery Login Verification',
                        f'Your login code is {otp}.',
                        None,
                        [customer.email],
                        fail_silently=False,
                    )
                except:
                    error_message = "Could not send email. Check SMTP settings."
                    request.session['is_otp_sent'] = False
                    return render(request, 'login.html', {'error': error_message})

                messages.info(request, f"Verification code sent to {customer.email}.")
                return render(request, 'login.html', {'is_otp_sent': True})

            else:
                return render(request, 'login.html', {'error': error_message, 'user_id': user_id})


# ================ PRODUCT DETAILS ==================
def productdetail(request, pk):
    totalitem = 0
    product = Product.objects.get(pk=pk)
    item_already_in_cart = False
    name = None

    if request.session.has_key('phone'):
        phone = request.session["phone"]
        totalitem = Cart.objects.filter(phone=phone).count()
        item_already_in_cart = Cart.objects.filter(product=product.id, phone=phone).exists()

        try:
            customer = Customer.objects.get(phno=phone)
            name = customer.name
        except:
            pass

    return render(request, 'productdetail.html', {
        'product': product,
        'item_already_in_cart': item_already_in_cart,
        'name': name,
        'totalitem': totalitem
    })


# ================= LOGOUT =======================
def logout(request):
    if request.session.has_key('phone'):
        del request.session["phone"]
    return redirect('login')


# ================= ADD TO CART ==================
def add_to_cart(request):
    if not request.session.has_key('phone'):
        return redirect('login')

    phone = request.session['phone']
    product_id = request.GET.get('prod_id')

    try:
        product_to_add = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect('homepage')

    existing_cart_item = Cart.objects.filter(phone=phone, product=product_to_add).first()

    if existing_cart_item:
        existing_cart_item.quantity += 1
        existing_cart_item.save()
    else:
        Cart(
            phone=phone,
            product=product_to_add,
            image=product_to_add.image,
            price=product_to_add.price,
            quantity=1
        ).save()

    return redirect(f"/product-detail/{product_id}")


# ================= SHOW CART (UPDATED FULLY) ==================
def show_cart(request):
    totalitem = 0
    name = None
    cart_items = []

    if request.session.has_key('phone'):
        phone = request.session["phone"]
        totalitem = Cart.objects.filter(phone=phone).count()

        try:
            customer = Customer.objects.get(phno=phone)
            name = customer.name
        except:
            pass

        cart_items = Cart.objects.filter(phone=phone)

        # ADD SUBTOTAL ATTRIBUTE
        for item in cart_items:
            item.subtotal = item.quantity * item.price

    data = {
        'name': name,
        'totalitem': totalitem,
        'cart': cart_items,
    }

    if cart_items:
        return render(request, 'show_cart.html', data)
    else:
        return render(request, 'empty_cart.html', data)


# ================= PLUS CART (returns subtotal) ==================
def plus_cart(request):
    if not request.session.has_key('phone'):
        return JsonResponse({'status': 'error'}, status=401)

    phone = request.session["phone"]
    cart_item_id = request.GET.get('prod_id')

    try:
        cart_item = Cart.objects.get(id=cart_item_id, phone=phone)
        cart_item.quantity += 1
        cart_item.save()

        subtotal = cart_item.quantity * cart_item.price

        return JsonResponse({
            'status': 'success',
            'quantity': cart_item.quantity,
            'subtotal': subtotal
        })

    except Cart.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)


# ================= MINUS CART (returns subtotal) ==================
def minus_cart(request):
    if not request.session.has_key('phone'):
        return JsonResponse({'status': 'error'}, status=401)

    phone = request.session["phone"]
    cart_item_id = request.GET.get('prod_id')

    try:
        cart_item = Cart.objects.get(id=cart_item_id, phone=phone)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

        subtotal = cart_item.quantity * cart_item.price

        return JsonResponse({
            'status': 'success',
            'quantity': cart_item.quantity,
            'subtotal': subtotal
        })

    except Cart.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)


# ================= REMOVE CART ==================
def remove_cart(request):
    if not request.session.has_key('phone'):
        return JsonResponse({'status': 'error'}, status=401)

    phone = request.session["phone"]
    cart_item_id = request.GET.get('prod_id')

    try:
        cart_item = Cart.objects.get(id=cart_item_id, phone=phone)
        cart_item.delete()

        new_total_items = Cart.objects.filter(phone=phone).count()

        return JsonResponse({
            'status': 'success',
            'totalitem': new_total_items
        })

    except Cart.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)


# ================= CHECKOUT ==================
def checkout(request):
    if not request.session.has_key('phone'):
        return redirect('login')

    if request.method == 'POST':
        request.session['shipping_info'] = {
            'name': request.POST.get('name'),
            'address': request.POST.get('address'),
            'mobile': request.POST.get('mobile'),
        }

        return render(request, 'checkout.html')

    return redirect('show-cart')


# ================= PAYMENT OTP ==================
def initiate_otp(request):
    if not request.session.has_key('phone'):
        return redirect('login')

    if request.method == 'POST':
        phone = request.session['phone']

        try:
            customer = Customer.objects.get(phno=phone)
        except:
            messages.error(request, "User session invalid.")
            return redirect('login')

        otp = str(random.randint(100000, 999999))
        request.session['payment_otp'] = otp

        try:
            send_mail(
                'SmartGrocery Payment Verification',
                f'Your OTP is {otp}',
                None,
                [customer.email],
                fail_silently=False,
            )
        except:
            messages.error(request, "Email sending failed.")

        return redirect('verify_otp')

    return redirect('homepage')


# ================= VERIFY OTP ==================
# def verify_otp_view(request):
#     if not request.session.has_key('phone'):
#         return redirect('login')
#
#     if 'payment_otp' not in request.session or 'shipping_info' not in request.session:
#         messages.error(request, "Session expired.")
#         return redirect('show-cart')
#
#     if request.method == 'POST':
#         user_otp = request.POST.get('otp_input')
#         session_otp = request.session.get('payment_otp')
#
#         if user_otp == session_otp:
#
#             phone = request.session['phone']
#             shipping = request.session['shipping_info']
#
#             customer = Customer.objects.get(phno=phone)
#             cart_items = Cart.objects.filter(phone=phone)
#             total_price = 0
#             for item in cart_items:
#                 item_subtotal = item.quantity * item.price
#                 total_price += item_subtotal
#                 OrderDetail(
#                     user=customer,
#                     product_name=item.product.name,
#                     qty=item.quantity,
#                     price=item_subtotal,
#                     image=item.image,
#                     address=shipping['address'],
#                     phone=shipping['mobile']
#                 ).save()
#
#             cart_items.delete()
#             del request.session['payment_otp']
#             del request.session['shipping_info']
#
#             # Inside verify_otp_view, near the top of the 'if user_otp == session_otp:' block
#             current_time = datetime.now().strftime("%Y-%m-%d %I:%M %p")
#             return redirect('order_success')
#
#         else:
#             return render(request, 'otp_verify.html', {'error': 'Wrong OTP'})
#
#     return render(request, 'otp_verify.html')

# ================= VERIFY OTP (UPDATED FOR BILLING) ==================
def verify_otp_view(request):
    if not request.session.has_key('phone'):
        return redirect('login')

    if 'payment_otp' not in request.session or 'shipping_info' not in request.session:
        messages.error(request, "Session expired.")
        return redirect('show-cart')

    if request.method == 'POST':
        user_otp = request.POST.get('otp_input')
        session_otp = request.session.get('payment_otp')

        if user_otp == session_otp:
            phone = request.session['phone']
            shipping = request.session['shipping_info']

            customer = Customer.objects.get(phno=phone)
            cart_items = Cart.objects.filter(phone=phone)

            # --- 🛠️ CALCULATION & BILL INITIALIZATION ---
            total_price = 0
            current_time = datetime.now().strftime("%Y-%m-%d %I:%M %p")

            # Start of the product table HTML
            product_table_html = """
                <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
                    <thead>
                        <tr style="border-bottom: 1px solid #ddd; background-color: #f2f2f2;">
                            <th style="padding: 8px; text-align: left;">Product</th>
                            <th style="padding: 8px; text-align: center;">Qty</th>
                            <th style="padding: 8px; text-align: right;">Unit Price (Rs)</th>
                            <th style="padding: 8px; text-align: right;">Subtotal (Rs)</th>
                        </tr>
                    </thead>
                    <tbody>
            """

            # --- 🛠️ LOOP FOR ORDER SAVE & BILL CONTENT GENERATION ---
            for item in cart_items:
                # Calculate the correct subtotal for this item
                item_subtotal = item.quantity * item.price
                total_price += item_subtotal  # Add to the running grand total

                # Save OrderDetail with the item's subtotal (fixing the price error)
                OrderDetail(
                    user=customer,
                    product_name=item.product.name,
                    qty=item.quantity,
                    price=item_subtotal,
                    image=item.image,
                    address=shipping['address'],
                    phone=shipping['mobile']
                ).save()

                # Build HTML row for the email bill
                product_table_html += f"""
                    <tr>
                        <td style="padding: 8px; text-align: left; border-bottom: 1px solid #eee;">{item.product.name}</td>
                        <td style="padding: 8px; text-align: center; border-bottom: 1px solid #eee;">{item.quantity}</td>
                        <td style="padding: 8px; text-align: right; border-bottom: 1px solid #eee;">{item.price}</td>
                        <td style="padding: 8px; text-align: right; border-bottom: 1px solid #eee; font-weight: bold;">{item_subtotal}</td>
                    </tr>
                """

            product_table_html += "</tbody></table>"  # Close the table body

            # --- 🛠️ STEP 3: PREPARE AND SEND EMAIL BILL ---

            # Minimalist HTML Structure for the Bill
            msg_html = f"""
                <html>
                <body style="font-family: Arial, sans-serif; font-size: 14px; color: #333; max-width: 600px; margin: auto; border: 1px solid #ddd; padding: 20px;">

                    <div style="overflow: auto;">
                        <span style="float: left; font-weight: bold; font-size: 16px;">Payment Method: Card/UPI</span>
                        <span style="float: right; font-weight: bold; font-size: 18px; color: #007bff;">SmartGrocery</span>
                    </div>
                    <hr style="border: none; border-top: 1px solid #eee; margin: 15px 0;">

                    <h3>Order Summary</h3>
                    <p><strong>Order Date/Time:</strong> {current_time}</p>
                    <p><strong>Billed To:</strong> {customer.name}</p>
                    <p><strong>Shipping Address:</strong> {shipping['address']}</p>
                    <p><strong>Contact Mobile:</strong> {shipping['mobile']}</p>

                    {product_table_html}

                    <div style="text-align: right; margin-top: 20px; padding-top: 10px; border-top: 2px solid #333;">
                        <p style="font-size: 18px; font-weight: bold; color: #28a745;">GRAND TOTAL: Rs. {total_price}</p>
                    </div>

                    <p style="text-align: center; margin-top: 30px; font-size: 12px; color: #999;">Thank you for shopping with SmartGrocery.</p>
                </body>
                </html>
            """

            # Send the email
            try:
                send_mail(
                    'SmartGrocery Order Confirmation (Bill)',
                    'Your order confirmation is attached.',
                    None,
                    [customer.email],
                    html_message=msg_html,
                    fail_silently=False,
                )
            except Exception as e:
                # This ensures your order still processes even if the email fails
                print(f"Error sending bill email: {e}")

                # Clear cart and session
            cart_items.delete()
            del request.session['payment_otp']
            del request.session['shipping_info']

            return redirect('order_success')

        else:
            return render(request, 'otp_verify.html', {'error': 'Wrong OTP'})

    return render(request, 'otp_verify.html')
# ================= ORDERS ==================
def orders_view(request):
    if not request.session.has_key('phone'):
        return redirect('login')

    phone = request.session['phone']
    customer = Customer.objects.get(phno=phone)
    orders = OrderDetail.objects.filter(user=customer).order_by('-ordered_date')

    return render(request, 'orders.html', {
        'orders': orders,
        'name': customer.name,
        'totalitem': 0,
    })


# ================= ORDER SUCCESS ==================
def order_success_view(request):
    return render(request, 'order_success.html')
