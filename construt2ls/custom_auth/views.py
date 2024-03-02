from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['pass_word']
        confirm_pass = request.POST['confirm_password']
        if password != confirm_pass:
            messages.warning(request, "Password not Matching")
            return render(request, 'signup.html')
        
        try:
            if User.objects.get(username=email):
                return HttpResponse('email already exist')
            
        except Exception as identifier:
            pass
        user = User.objects.create_user(email, email, password)
        user.save()
        return HttpResponse("User created", email)
    return render(request, "signup.html")
    

def handlelogin(request):
    return render(request, "login.html")

def handlelogout(request):
    return redirect(request, '/auth/login')