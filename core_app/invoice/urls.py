from django.urls import path
from .views import InvoiceViews, InvoiceProductViews, InvoicePrint, InvoiceHistoryViews, InvoiceSendViews, InvoiceDetailViews, InvoiceHistoryDetailViews

app_name = "invoice"

urlpatterns = [
    path('', InvoiceViews.as_view(template_name="index_invoice.html"), name="index"),
    path('create/', InvoiceViews.as_view(template_name="add_invoice.html"), name="store"),
    path('update/<int:id>', InvoiceViews.as_view(template_name="add_invoice.html"), name="update"),
    path('products/<int:id>', InvoiceProductViews.as_view(template_name="add_invoice.html"), name="index-product"),
    path('products/create/<int:id>', InvoiceProductViews.as_view(template_name="add_invoice.html"), name="store-product"),
    path('products/delete/<int:id>', InvoiceProductViews.as_view(template_name="add_invoice.html"), name="delete-product"),
    path('print/<int:id>', InvoicePrint.as_view(template_name="print_invoice.html"), name="print-invoice"),
    path('send/<int:id>', InvoiceSendViews.as_view(template_name="send_invoice.html"), name="send"),
    path('detail/<int:id>', InvoiceDetailViews.as_view(template_name="detail_invoice.html"), name="detail"),
    path('history/', InvoiceHistoryViews.as_view(template_name="history_invoice.html"), name="history"),
    path('history/detail/<int:id>', InvoiceHistoryDetailViews.as_view(template_name="history_detail_invoice.html"), name="history-detail"),
]