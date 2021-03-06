from django.contrib.auth import views as auth_views
from django.urls import path

from users import views

urlpatterns = [path('signup/', views.SignUp.as_view(), name='signup'),
               path('login/', auth_views.LoginView.as_view(), name='login'),
               path('logout/', auth_views.LogoutView.as_view(), name='logout'),
               path('password_change/',
                    auth_views.PasswordChangeView.as_view(),
                    name='password_change'),
               path('password_change/done/',
                    auth_views.PasswordChangeDoneView.as_view(),
                    name='password_change_done'),
               path('password_reset/', auth_views.PasswordResetView.as_view(),
                    name='password_reset'),
               path('password_reset/done/',
                    auth_views.PasswordResetDoneView.as_view(),
                    name='password_reset_done'),
               path('reset/<str:uidb64>/<str:token>/',
                    auth_views.PasswordResetConfirmView.as_view(),
                    name='password_reset_confirm'),
               path('reset/done/',
                    auth_views.PasswordResetCompleteView.as_view(),
                    name='password_reset_complete')]
