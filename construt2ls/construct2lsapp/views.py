from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from math import ceil
from construct2lsapp.models import Contact, Product, OrderUpdate, Orders
from construct2lsapp import keys
import time  # Import the time module for generating timestamps

# Views for handling different pages and actions

# View for the home page
def index(request):
    # Logic to retrieve products and organize them for display
    allprods = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allprods.append([prod, range(1, nSlides), nSlides])

    params = {'allprods': allprods}  # Parameters to be passed to the template
    return render(request, "index.html", params)


# View for the contact page
def contact(request):
    # Handle form submission for contacting
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        desc = request.POST.get("desc")
        phone_number = request.POST.get("phone_number")
        # Save the contact details
        myquery = Contact(name=name, email=email, description=desc, phone_num=phone_number)
        myquery.save()
        messages.info(request, "Thank you for contacting us, we will get back to you soon...")
        return render(request, "contact.html")
    return render(request, "contact.html")


# View for the about page
def about(request):
    return render(request, "about.html")


# View for the blog page
def blog(request):
    return render(request, "blog.html")


# Function to generate a unique order ID based on timestamp
def generate_unique_order_id():
    return str(int(time.time()))  # Using timestamp as order ID


# View for the checkout page
def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/auth/login')

    # Handle form submission for checkout
    if request.method == "POST":
        # Retrieve order details from the form
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        # Save order details
        Orders.objects.create(
            items_json=items_json,
            name=name,
            amount=amount,
            email=email,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            zip_code=zip_code,
            phone=phone
        )

        # Prepare payment data for redirection
        payment_data = {
            'MID': keys.MID,  # Your Flutterwave Merchant ID
            'ORDER_ID': generate_unique_order_id(),  # Generate a unique order ID
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',
        }

        # Redirect user to a payment page
        return render(request, 'flutterwave_payment.html', {'payment_data': payment_data})

    return render(request, 'checkout.html')


# View for handling payment requests from Flutterwave
@csrf_exempt
def handlerequest(request):
    if request.method == 'POST':
        form = request.POST

        status = form.get('STATUS', '')
        if status == 'successful':
            order_id = form.get('ORDER_ID')
            amount_paid = form.get('TXN_AMOUNT')
            try:
                order = Orders.objects.get(order_id=order_id)
            except Orders.DoesNotExist:
                return HttpResponseBadRequest('Order not found')

            if float(amount_paid) == order.amount:
                order.status = 'paid'
                order.amount_paid = amount_paid
                order.save()
                return JsonResponse({'status': 'success', 'message': 'Payment successful'}, status=200)
            else:
                return HttpResponseBadRequest('Amount paid does not match the order total')
        else:
            return JsonResponse({'status': 'error', 'message': 'Payment unsuccessful'}, status=400)

    else:
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)


# View for the profile page
def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/auth/login')

    currentUser = request.user.username
    items = Orders.objects.filter(email=currentUser)
    rid = ""
    for i in items:
        myid = i.oid 
        rid = myid.replace("ShopyCart", "")

    status = None  # Initialize status to None
    if rid:  # Check if rid is not an empty string
        try:
            rid_int = int(rid)  # Convert rid to integer
            status = OrderUpdate.objects.filter(order_id=rid_int)
        except ValueError:
            pass

    context = {"items": items, "status": status}  # Include status in the context
    return render(request, "profile.html", context)
