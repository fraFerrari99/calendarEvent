from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('sign_in', auth_views.LoginView.as_view(template_name="user/login.html"), name='sign_in'),
    path('sign_out', views.logout_view, name='sign_out'),
    path('profile/<str:email>', views.profile, name='profile'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('change_password',views.change_password,name="change_password"),
    path('forgot_pwd',views.forgot_password,name="forgot_pwd"),
    path('password_reset_confirm/<uidb64>/<token>', views.password_reset_confirm, name='password_reset_confirm'),
    path('change_email', views.change_email, name="change_email"),
]
