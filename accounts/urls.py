from django.urls import path
from accounts import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('activate/<str:uidb64>/<str:token>/', views.activate_account, name='activate'),
    path('Registration/', views.register, name='Registration'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('ChangePassword/',views.ChangePasswordView.as_view() , name = 'ChangePassword' ),
    path('password_reset/', views.password_reset_view, name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
    path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),
    path('terms-and-condition/', views.terms_and_condition, name='terms-and-condition'),
    path('check_error/', views.error_view, name='check-error'),

]
