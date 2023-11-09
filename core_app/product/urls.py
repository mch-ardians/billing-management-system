from django.urls import path
from .views import ProductViews

app_name = "product"

urlpatterns = [
    path('', ProductViews.as_view(template_name="index_product.html"), name='index'),
    path('create/', ProductViews.as_view(template_name="add_product.html"), name='store'),
    path('update/<int:id>', ProductViews.as_view(template_name="edit_product.html"), name='update'),
    path('delete/<int:id>', ProductViews.as_view(), name='delete')
]