from django.urls import path, include

from . import views
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
    path('', views.dashboard, name='dashboard'),
    path('accounts/', views.include('django.contrib.auth.urls')),
    path('account/register/', views.register, name='register'),
    path('account/edit/', views.edit, name='edit'),
    path('account/users/', views.user_list, name='user_list'),
    path('account/users/follow/', views.user_follow, name='user_follow'),
    path('account/users/<slug:slug>-<uuid:uuid>/', views.user_detail, name='user_detail'),
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