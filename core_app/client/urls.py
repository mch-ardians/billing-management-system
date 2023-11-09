from django.urls import path
from .views import ClientViews

app_name = "client"

urlpatterns = [
    path('', ClientViews.as_view(template_name='index_client.html'), name='index'),
    path('create/', ClientViews.as_view(template_name='add_client.html'), name='store'),
    path('update/<int:id>', ClientViews.as_view(template_name='edit_client.html'), name='update'),
    path('delete/<int:id>', ClientViews.as_view(), name='delete'),
]