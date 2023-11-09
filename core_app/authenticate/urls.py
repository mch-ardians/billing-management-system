from django.urls import path
from . import views

app_name = "authenticate"

urlpatterns = [
    path('login/', views.sign_in, name="login"),
    path("logout/", views.sign_out, name="logout"),
]