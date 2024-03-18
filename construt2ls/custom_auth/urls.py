"""
from django.urls import path
from custom_auth import views


urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.handlelogin, name="login"),
    path('logout/', views.handlelogout, name="logout"),
    path('activate/<uidb64>/<token>/', views.ActivateAccountView.as_view(), name='activate'),
    path('request-reset-email/',views.RequestResetEmailView.as_view(),name='request-reset-email'),
    path('set-new-password/<uidb64>/<token>',views.SetNewPasswordView.as_view(),name='set-new-password'),

]
"""
from django.urls import path
from custom_auth import views

urlpatterns = [
    # URL pattern for user signup
    path('signup/', views.signup, name="signup"),

    # URL pattern for user login
    path('login/', views.handlelogin, name="login"),

    # URL pattern for user logout
    path('logout/', views.handlelogout, name="logout"),

    # URL pattern for requesting a password reset email
    path('request-reset-email/', views.RequestResetEmailView.as_view(), name='request-reset-email'),

    # URL pattern for setting a new password (with parameters for UID and token)
    path('set-new-password/<uidb64>/<token>/', views.SetNewPasswordView.as_view(), name='set-new-password'),

    # URL pattern for activating an account (REMOVE THIS LINE)
    # Remove the URL pattern for ActivateAccountView
]

