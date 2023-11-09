from django.urls import path
from .views import SettingViews, SettingProductViews

app_name = "setting"

urlpatterns = [
    path('', SettingViews.as_view(template_name="index_setting.html"), name="index"),
    path('products/<int:id>', SettingProductViews.as_view(template_name="add_setting.html")),
    path('create/', SettingViews.as_view(template_name="add_setting.html"), name="store"),
    path('update/<int:id>', SettingViews.as_view(template_name="edit_setting.html"), name="update"),
    path('run/<int:id>', SettingViews.as_view(template_name="index_setting.html"), name="run"),
]