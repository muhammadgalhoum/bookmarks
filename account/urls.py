from django.urls import path, include

from .views import *
# from django.contrib.auth.views import (
#     LoginView, 
#     LogoutView, 
#     PasswordChangeView,
#     PasswordChangeDoneView,
#     PasswordResetView,
#     PasswordResetDoneView,
#     PasswordResetConfirmView,
#     PasswordResetCompleteView,
# )

app_name = 'account'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('account/register/', register, name='register'),
    path('account/edit/', edit, name='edit'),
    path('account/users/', user_list, name='user_list'),
    path('account/users/follow/', user_follow, name='user_follow'),
    path('account/users/<slug:slug>-<uuid:uuid>/',user_detail, name='user_detail'),
]

# path('login/', LoginView.as_view(), name='login'),
# path('logout/', LogoutView.as_view(), name='logout'),
# path('password-change/', PasswordChangeView.as_view(),
#     name='password_change'),
# path('password-change/done/', PasswordChangeDoneView.as_view(),
#     name='password_change_done'),
# path('password-reset/', PasswordResetView.as_view(),
#     name='password_reset'),
# path('password-reset/done/', PasswordResetDoneView.as_view(),
#     name='password_reset_done'),
# path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
#     name='password_reset_confirm'),
# path('password-reset/complete/', PasswordResetCompleteView.as_view(),
#     name='password_reset_complete'),