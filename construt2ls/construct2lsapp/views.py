from django.shortcuts import render
from construct2lsapp.models import Contact, Product
from django.contrib import messages
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