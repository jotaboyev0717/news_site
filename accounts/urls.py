from django.urls import path
from .views import edit_user, user_login, user_logout, dashboard_view, user_register, SignUpView, EditUserView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetView, \
    PasswordResetCompleteView
# from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', dashboard_view, name='user_profile'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change_done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register/', user_register, name='register'),
    path('profile/edit/', EditUserView.as_view(), name='edit_user'),
    # path('profile/edit/', edit_user, name='edit_user'),
    # path('register/', SignUpView.as_view(), name='register'),
    # path('login/', LoginView.as_view(template_name='account/login.html', http_method_names=['get', 'post']), name='login'),
    # path('logout/', LogoutView.as_view(template_name='account/logged_out.html'), name='logout')
]
