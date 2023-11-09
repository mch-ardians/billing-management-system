from django.urls import path
from .views import ProfileViews

app_name = "bioprofile"

urlpatterns = [
    path('<int:id>', ProfileViews.as_view(template_name="index_profile.html"), name='index'),
    path('update/<int:id>', ProfileViews.as_view(template_name="ined_profile.html"), name='update'),
    path('delete/<int:id>', ProfileViews.as_view(), name='delete'),
]