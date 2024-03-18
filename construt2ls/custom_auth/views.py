from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.views.generic import View
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

# Get the user model
User = get_user_model()

# View for user signup
def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['pass_word']
        confirm_pass = request.POST['confirm_password']
        if password != confirm_pass:
            messages.warning(request, "Password not Matching")
            return render(request, 'signup.html')
        
        # Attempt to create a new user or get existing user
        user, created = User.objects.get_or_create(username=email, email=email)
        if created:
            user.set_password(password)
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, "Account created and logged in successfully")
            return redirect('/')
        else:
            messages.info(request, "Account already exists. Please log in.")
            return redirect('/auth/login')
    return render(request, "signup.html")


# View for user login
def handlelogin(request):
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['pass_word']
        my_user = authenticate(username=username, password=password)

        if my_user is not None:
            login(request, my_user)
            messages.success(request, 'Login Successful')
            return redirect('/')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('/auth/login')
    return render(request, 'login.html')


# View for user logout
def handlelogout(request):
    logout(request)
    messages.info(request, "You have successfully logged out")
    return redirect('/auth/login')


# View for requesting a password reset email
class RequestResetEmailView(View):
    def get(self, request):
        return render(request, 'request-reset-email.html')
    
    def post(self, request):
        email = request.POST.get('email')

        user = User.objects.filter(email=email).first()
        if user:
            # Generate a password reset token
            token_generator = PasswordResetTokenGenerator()
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)

            # Construct the password reset link
            reset_link = request.build_absolute_uri(
                f'/auth/set-new-password/{uidb64}/{token}'
            )

            # Send the password reset link to the user via email
            email_subject = '[Reset Your Password]'
            email_message = f"Please click the link below to reset your password:\n\n{reset_link}"
            # Send email using your preferred method, e.g., Django's EmailMessage

            messages.info(request, "We have sent you an email with instructions on how to reset the password.")
            return render(request, 'request-reset-email.html')

        # If the email is not found, still show success message to avoid information leakage
        messages.info(request, "If the provided email exists in our system, we have sent you an email with instructions on how to reset the password.")
        return render(request, 'request-reset-email.html')


# View for setting a new password
class SetNewPasswordView(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.warning(request, "Password Reset Link is Invalid")
                return redirect('/auth/request-reset-email/')  # Redirect to request reset email page

        except Exception as e:
            messages.error(request, "Something Went Wrong")
            return redirect('/auth/login/')  # Redirect to login page

        return render(request, 'set-new-password.html', context)
    

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']

        if password != confirm_password:
            messages.warning(request, "Password is Not Matching")
            return render(request, 'set-new-password.html', context)

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request, "Password Reset Success Please Login with New Password")
            return redirect('/auth/login/')

        except Exception as e:
            messages.error(request, "Something Went Wrong")
            return redirect('/auth/login/')

        return render(request, 'set-new-password.html', context)
