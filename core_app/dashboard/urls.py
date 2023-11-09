from django.urls import path
from .views import DashboardViews

app_name = "dashboard"

urlpatterns = [
    path('', DashboardViews.as_view(template_name="index.html"), name="index"),
    path("delete/<int:id>", DashboardViews.as_view(template_name="index.html"), name="delete"),
]