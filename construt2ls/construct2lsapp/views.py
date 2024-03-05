from django.shortcuts import render
from construct2lsapp.models import Contact
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, "index.html")



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