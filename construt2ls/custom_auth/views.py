from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import TokenGenerator, generate_token
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.conf import settings

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
                #return HttpResponse('email already exist')
                messages.info(request, "Sorry, that email is already in use")
                return render(request, 'signup.html')
                
            
        except Exception as identifier:
            pass
        user = User.objects.create_user(email, email, password)
        user.is_active=False
        user.save()
        email_subject="Activate Your Account"
        message = render_to_string('auth/activate.html', {
            'user': user,
            'domain': '127.0.0.1:8000',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        })

        email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email],)
        email_message.send()
        messages.success(request, "Activate Your Accout by clicking the link in your gmail")
        return redirect('/auth/login')

        return HttpResponse("User created", email)
    return render(request, "signup.html")
    

def handlelogin(request):
    return render(request, "login.html")

def handlelogout(request):
    return redirect(request, '/auth/login')