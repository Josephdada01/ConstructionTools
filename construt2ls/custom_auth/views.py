from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import TokenGenerator, generate_token
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import authenticate, login, logout

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

        # This is what i added
        # generate_token = PasswordResetTokenGenerator()
        # token = generate_token.make_token(user)

        email_subject="Activate Your Account"
        message = render_to_string('auth/activate.html', {
            'user': user,

            'domain': '127.0.0.1:8000',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
            #'domain': request.get_host(),
            #'uid': urlsafe_base64_encode(user.pk.encode()),
            #'token': token
        })

        email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email],)
        email_message.send()
        messages.success(request, "Activate Your Accout by clicking the link in your gmail")
        return redirect('/auth/login')
    return render(request, "signup.html")



class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.info(request, "Account Activated Sucessfully")
            return redirect('/auth/login')
        return render(request, 'activatefail.html')
    

def handlelogin(request):
    if request.method == "POST":
        
        username = request.POST['email']
        userpassword = request.POST['pass_word']
        my_user = authenticate(username = username, password = userpassword)

        if my_user is not None:
            login(request, my_user)
            messages.success(request, 'Login Successful')
            return redirect('/')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('/auth/login')
    return render(request, 'login.html')





def handlelogout(request):
    return redirect(request, '/auth/login')