"""
@csrf_exempt
def checkout(request):
    from flutterwave import Flutterwave  # Import moved inside the function

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

        # Initialize Flutterwave
        flutterwave = Flutterwave(public_key='FLWPUBK_TEST-45e7643c3a43b48aa033918df7fabf23-X',
                                  secret_key='FLWSECK_TEST-ad146de7a6dd343642fbfe9f07c1e260-X', environment='sandbox')

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
"""


"""
from django.shortcuts import render, redirect
from construct2lsapp.models import Contact, Product, OrderUpdate, Orders
from django.contrib import messages
from flutterwave import Flutterwave
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from math import ceil

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

        # Initialize Flutterwave
        flutterwave = Flutterwave(public_key='YOUR_FLUTTERWAVE_PUBLIC_KEY', secret_key='YOUR_FLUTTERWAVE_SECRET_KEY', environment='sandbox')

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


def verify_flutterwave_checksum(data, checksum):
    # Verify the checksum using Flutterwave SDK or your preferred method
    # Example using Flutterwave SDK:
    flutterwave = Flutterwave(public_key='FLWPUBK_TEST-45e7643c3a43b48aa033918df7fabf23-X', secret_key='FLWSECK_TEST-ad146de7a6dd343642fbfe9f07c1e260-X', environment='sandbox')
    is_valid_checksum = flutterwave.Transaction.verify_checksum(data, checksum)
    return is_valid_checksum


 This is the implementation of Paytm
def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/auth/login')

    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2','')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        Order = Orders(items_json=items_json,name=name,amount=amount, email=email, address1=address1,address2=address2,city=city,state=state,zip_code=zip_code,phone=phone)
        print(amount)
        Order.save()
        update = OrderUpdate(order_id=Order.order_id,update_desc="the order has been placed")
        update.save()
        thank = True

    # # PAYMENT INTEGRATION

        id = Order.order_id
        oid=str(id)+"ShopyCart"
        param_dict = {

            'MID':keys.MID,
            'ORDER_ID': oid,
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'paytm.html', {'param_dict': param_dict})

    return render(request, 'checkout.html')


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
            a=response_dict['ORDERID']
            b=response_dict['TXNAMOUNT']
            rid=a.replace("ShopyCart","")
           
            print(rid)
            filter2= Orders.objects.filter(order_id=rid)
            print(filter2)
            print(a,b)
            for post1 in filter2:

                post1.oid=a
                post1.amountpaid=b
                post1.paymentstatus="PAID"
                post1.save()
            print("run agede function")
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'paymentstatus.html', {'response': response_dict})
"""
