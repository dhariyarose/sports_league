from user_register import views
from django.urls import path, include

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

]
