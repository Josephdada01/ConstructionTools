from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from math import ceil
from construct2lsapp.models import Contact, Product, OrderUpdate, Orders
from construct2lsapp import keys
#from flutter.Checksum import generate_checksum
import time  # Import the time module for generating timestamps


# Create your views here.
def index(request):
    allprods = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allprods.append([prod, range(1, nSlides), nSlides])

    params = {'allprods': allprods}

    return render(request, "index.html", params)


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        desc = request.POST.get("desc")
        phone_number = request.POST.get("phone_number")
        myquery = Contact(name=name, email=email, description=desc, phone_num=phone_number)
        myquery.save()
        messages.info(request, "Thank you for contacting us, we will get back to you soon...")
        return render(request, "contact.html")
    return render(request, "contact.html")


def about(request):
    return render(request, "about.html")


def generate_unique_order_id():
    """
    Generate a unique order ID based on timestamp.
    """
    
    
    return str(int(time.time()))  # Using timestamp as order ID


def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/auth/login')

    if request.method == "POST":
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
        thank = True

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

@csrf_exempt
def handlerequest(request):
    if request.method == 'POST':
        form = request.POST

        status = form.get('STATUS', '')
        if status == 'successful':
            order_id = form.get('ORDER_ID')
            amount_paid = form.get('TXN_AMOUNT')
            # Retrieve the order from the database based on the order ID
            try:
                order = Orders.objects.get(order_id=order_id)
            except Orders.DoesNotExist:
                return HttpResponseBadRequest('Order not found')

            # Compare the amount paid with the total amount of the order
            if float(amount_paid) == order.amount:
                # Update order status in the database
                order.status = 'paid'
                order.amount_paid = amount_paid
                order.save()
                return JsonResponse({'status': 'success', 'message': 'Payment successful'}, status=200)
            else:
                # Amount paid doesn't match the order total
                # Handle the discrepancy (e.g., log, notify customer, etc.)
                return HttpResponseBadRequest('Amount paid does not match the order total')
        else:
            return JsonResponse({'status': 'error', 'message': 'Payment unsuccessful'}, status=400)

    else:
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
            # Update order status in the database
            #try:
                #order = Orders.objects.get(order_id=order_id)
                #order.status = 'paid'
                #order.amount_paid = amount_paid
                #order.save()
                #return JsonResponse({'status': 'success', 'message': 'Payment successful'}, status=200)
            #except Orders.DoesNotExist:
                #return JsonResponse({'status': 'error', 'message': 'Order not found'}, status=404)
        #else:
            #return JsonResponse({'status': 'error', 'message': 'Payment unsuccessful'}, status=400)

    #else:
        #return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

"""
@csrf_exempt
def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/auth/login')

    if request.method == "POST":
        from flutterwave import Flutterwave  # Import Flutterwave here to avoid circular import

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
        thank = True

        # Initialize Flutterwave
        flutterwave = Flutterwave(public_key=keys.pk ,
                                  secret_key=keys.sk , environment='sandbox')

        # Construct payment data
        payment_data = {
            "amount": amount,
            "currency": "NGN",  # Update currency as per your requirement
            "payment_options": "card, banktransfer, ussd",  # Add supported payment options
            "customer": {
                "email": email,
                "name": name,
            },
            "customizations": {
                "title": "My Store",
                "description": "Payment for items in cart",
            }
        }

        # Create payment request
        response = flutterwave.Transaction.initiate(data=payment_data)

        # Redirect user to Flutterwave payment page
        return redirect(response['data']['link'])

    return render(request, 'checkout.html')


@csrf_exempt
def handlerequest(request):
    def verify_flutterwave_checksum(data, checksum):
        from flutterwave import Flutterwave  # Import moved inside the function

        # Verify the checksum using Flutterwave SDK or your preferred method
        # Example using Flutterwave SDK:
        flutterwave = Flutterwave(public_key=keys.pk,
                                  secret_key=keys.sk, environment='sandbox')
        is_valid_checksum = flutterwave.Transaction.verify_checksum(data, checksum)
        return is_valid_checksum

    if request.method == 'POST':
        # Extract data from the request
        form = request.POST
        response_dict = {}
        for i in form.keys():
            response_dict[i] = form[i]
            if i == 'CHECKSUMHASH':
                checksum = form[i]

        # Verify the payment checksum
        verify = verify_flutterwave_checksum(response_dict, checksum)

        if verify:
            # Payment checksum is valid
            if response_dict.get('status') == 'successful':

                thank = True
                
                # Payment was successful, update your database accordingly
                order_id = response_dict.get('order_id')
                amount_paid = response_dict.get('amount')
                # Example:
                order = Orders.objects.get(id=order_id)
                order.status = 'paid'
                order.amount_paid = amount_paid
                order.save()

                # Log the success
                print('Order successful:', order_id)

            else:
                # Payment was not successful
                error_message = response_dict.get('message')
                # Log the error
                print('Order not successful:', error_message)

        else:
            # Checksum verification failed, possibly a fraudulent request
            # Log the error
            print('Invalid checksum. Possible fraudulent request')

        # Return a JSON response indicating success or failure
        return JsonResponse({'status': 'success'}, status=200)

    else:
        # Only accept POST requests
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

# Define the generate_unique_order_id function
def generate_unique_order_id():
    
    Generate a unique order ID based on timestamp.
    
    return str(int(time.time()))  # Using timestamp as order ID


@csrf_exempt
def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/auth/login')

    if request.method == "POST":
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
        thank = True

        checksum_data = {
            'MID': keys.MID,  # Your Flutterwave Merchant ID
            'ORDER_ID': generate_unique_order_id(),  # Generate a unique order ID
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',
        }
        checksum = generate_checksum(checksum_data, keys.MK)
        # Include the checksum in the payment data
        payment_data = {
            **checksum_data,
            'CHECKSUMHASH': checksum,
        }

        # Redirect user to Flutterwave payment page
        return render(request, 'flutterwave_payment.html', {'payment_data': payment_data})

    return render(request, 'checkout.html')

@csrf_exempt
def handlerequest(request):
    if request.method == 'POST':
        form = request.POST

        # Verify checksum
        checksum = form.get('CHECKSUMHASH', '')
        if not checksum.verify_checksum(form, keys.MK, checksum):
            return JsonResponse({'status': 'error', 'message': 'Invalid checksum'}, status=400)

        # Handle payment response
        status = form.get('STATUS', '')
        if status == 'successful':
            order_id = form.get('ORDERID')
            amount_paid = form.get('TXNAMOUNT')
            # Update order status in the database
            try:
                order = Orders.objects.get(order_id=order_id)
                order.status = 'paid'
                order.amount_paid = amount_paid
                order.save()
                return JsonResponse({'status': 'success', 'message': 'Payment successful'}, status=200)
            except Orders.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Order not found'}, status=404)
        else:
            return JsonResponse({'status': 'error', 'message': 'Payment unsuccessful'}, status=400)

    else:
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

"""


"""def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/auth/login')
    
    currentUser = request.user.username
    items = Orders.objects.filter(email = currentUser)
    rid=""
    for i in items:
        print(i.order_id )
        # print(i.order_id)
        myid=i.order_id 
        rid=myid.replace("ShopyCart","")
        print(rid)
    status=OrderUpdate.objects.filter(order_id=int(rid))
    for j in status:
        print(j.update_desc)
    context = {"items": items}
    print(currentUser)
    return render(request, "profile.html", context)
"""

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
            # Handle the case where rid cannot be converted to an integer
            # Log the error or handle it appropriately
            pass

    context = {"items": items, "status": status}  # Include status in the context
    return render(request, "profile.html", context)
