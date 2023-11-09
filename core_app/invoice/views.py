from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.db.models import Sum, F, ExpressionWrapper, IntegerField
from django.db.models import Q
from .forms import FormInvoice, FormClientsProduct, SendInvoiceForm, DetailInvoiceForm, PaymentForm
from .models import Invoice, ClientsProduct, ClientsPayment
from product.models import Product
from django.template.loader import render_to_string
import json, os

# Create your views here.
class InvoiceViews(View):
    template_name = ""
    
    def get(self, request, id=None):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        query = Invoice.objects.annotate(
        client_name=F('client__nama'),
        total_price=Sum(F('clientsproduct__price') * F('clientsproduct__quantity'))
        ).values(
            'id',
            'client_name', 
            'invoice_date', 
            'invoice_num', 
            'total_price', 
            'status'
        ).filter(status="Active")
        
        if is_ajax:
            search_value = request.GET.get('search[value]')
            if search_value:
                query = query.filter(nama__icontains=search_value)

            start = int(request.GET.get('start', 0))
            length = int(request.GET.get('length', 10))
            page_data = query[start:start+length]

            data = []
            for invoice in page_data:
                product_name = list(ClientsProduct.objects.filter(invoice=invoice["id"]).values_list('product__nama_product', flat=True))
                products = ', '.join(product_name)
                
                data.append({
                    'DT_RowIndex': start + 1,
                    'nama': invoice["client_name"],
                    'product': products,
                    'invoice_date': invoice["invoice_date"],
                    'no_invoice': invoice["invoice_num"],
                    'total': invoice["total_price"],
                    'status': invoice["status"],
                    'action': f"""
                                    <div class="dropdown position-relative">
                                        <button class="btn btn-outline border border-0" data-bs-toggle="dropdown" data-bs-display="static">
                                            <i class="align-middle" data-feather="more-vertical"></i>
                                        </button>
                                        <div class="dropdown-menu dropdown-menu-end">
                                            <button class="dropdown-item" id="btn_detail" value="{ invoice["id"] }">Detail</button>
                                        </div>
                                    </div>
                              """
                })
                start += 1
                
            return JsonResponse({
                'draw': int(request.GET.get('draw', 1)),
                'recordsTotal': query.count(),
                'recordsFiltered': query.count(),
                'data': data,
            })
        
        form_invoice = FormInvoice()
        form_clients_product = FormClientsProduct()
        
        context = {
            "title": "Invoice",
            "invoice_no_invoice_form": form_invoice["no_invoice"],
            "invoice_client_form": form_invoice["client"],
            "invoice_date_form": form_invoice["invoice_date"],
            "invoice_due_form": form_invoice["due_date"],
            "clients_product_product_form": form_clients_product["product"],
            "clients_product_item_form": form_clients_product["item"],
            "clients_product_qty_form": form_clients_product["qty"],
            "clients_product_price_form": form_clients_product["price"],
        }
          
        return render(request, self.template_name, context)
    
    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if is_ajax:
            data = json.loads(request.body.decode('utf-8')) if request.body else {}
            payload = data.get('payload', {})
            
            form_invoice = FormInvoice(payload)
            
            if form_invoice.is_valid():
                invoice = Invoice.objects.create(
                    invoice_num = form_invoice.cleaned_data["no_invoice"],
                    client = form_invoice.cleaned_data["client"],
                    invoice_date = form_invoice.cleaned_data["invoice_date"],
                    due_date = form_invoice.cleaned_data["due_date"],
                    status = "Pending",
                )
                
                return JsonResponse({'message': 'Congratulations! Your invoice has been added!', 'invoice_id': invoice.id})
            else:
                return JsonResponse({'errors': {**form_invoice.errors}}, status=400)
    
    def put(self, request, id):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        values = Invoice.objects.get(id=id)
        
        if is_ajax:
            data = json.loads(request.body.decode('utf-8')) if request.body else {}
            payload = data.get('payload', {})
            
            form_invoice = FormInvoice(payload)
            
            if form_invoice.is_valid():
                values.invoice_num = form_invoice.cleaned_data["no_invoice"]
                values.client = form_invoice.cleaned_data["client"]
                values.invoice_date = form_invoice.cleaned_data["invoice_date"]
                values.due_date = form_invoice.cleaned_data["due_date"]
                values.save()
                
                return JsonResponse({'message': 'Congratulations! Your invoice has been changed!'})
            else:
                return JsonResponse({'errors': {**form_invoice.errors}}, status=400)
    
class InvoiceProductViews(View):
    template_name = ""
    
    def get(self, request, id):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if is_ajax:
            products = Product.objects.select_related("client").filter(client_id=id).all()
            
            data = [{"id": product.id, "nama_product": product.nama_product} for product in products]
            
            if len(data) != 0:
                return JsonResponse(data, safe=False)
            else:
                return JsonResponse(data=[{"id": "undefined", "nama_product": "undefined"}], safe=False)
    
    def post(self, request, id):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if is_ajax:
            data = json.loads(request.body.decode('utf-8')) if request.body else {}
            payload = data.get('payload', {})
            
            form_product = FormClientsProduct(payload)
            
            if form_product.is_valid():
                ClientsProduct.objects.create(
                    product = form_product.cleaned_data["product"],
                    invoice = Invoice.objects.get(pk=id),
                    item = form_product.cleaned_data["item"],
                    quantity = form_product.cleaned_data["qty"],
                    price = form_product.cleaned_data["price"],
                )
                
                queryset = ClientsProduct.objects.filter(invoice=id).select_related("product").annotate(result=ExpressionWrapper(F('price') * F('quantity'), output_field=IntegerField()))
                queryset_totals = ClientsProduct.objects.filter(invoice=id).aggregate(total_quantity=Sum('quantity'), total_subtotal=Sum(ExpressionWrapper(F('price') * F('quantity'), output_field=IntegerField())))
                
                html = render_to_string('list_product.html', {"list_views": queryset})
                
                return JsonResponse({'html': html, 'total_qty': queryset_totals["total_quantity"], 'total_subtotal': queryset_totals["total_subtotal"]})
            else:
                return JsonResponse({'errors': {**form_product.errors}}, status=400)
    
    def delete(self, request, id):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if is_ajax:
            get_object_or_404(ClientsProduct, id=id).delete() 
            
            return JsonResponse({'message': 'Congratulations! Your clients product has been deleted!'})
   
class InvoicePrint(View):
    template_name = ""
    
    def get(self, request, id):
        queryset = ClientsProduct.objects.filter(invoice=id).select_related("product").annotate(result=ExpressionWrapper(F('price') * F('quantity'), output_field=IntegerField()))
        queryset_totals = ClientsProduct.objects.filter(invoice=id).aggregate(total_subtotal=Sum(ExpressionWrapper(F('price') * F('quantity'), output_field=IntegerField())))
        tax = 0.15 * queryset_totals["total_subtotal"]
        subtotal = queryset_totals["total_subtotal"] + tax
        queryset_detail = ClientsProduct.objects.filter(invoice=id).select_related("invoice").first()
        queryset_client = Invoice.objects.filter(id=id).select_related("client", "client__alamat").get()

        context = {
                "title" : "Invoice",
                "list_views" : queryset,
                "total_subtotal" : queryset_totals["total_subtotal"],
                "tax" : int(tax),
                "subtotal" : int(subtotal),
                "no_invoice" : queryset_detail.invoice.invoice_num,
                "invoice_date" : queryset_detail.invoice.invoice_date,
                "due_date" : queryset_detail.invoice.due_date,
                "client" : queryset_client.client.nama,
                "jalan" : queryset_client.client.alamat.jalan,
                "no_telp" : queryset_client.client.no_wa
        }
        
        return render(request, self.template_name, context) 
    
class InvoiceSendViews(View):
    template_name = ""
    
    def get(self, request, id):
        values = Invoice.objects.select_related("client").get(id=id)
        
        invoice_values = {
            "client": values.client,
            "email": values.client.email,
            "no_wa": values.client.no_wa,
        }    
            
        form_send_invoice = SendInvoiceForm(initial=invoice_values, invoice_id=id)
            
        context = {
            "title" : "Invoice",
            "client_form" : form_send_invoice["client"],
            "email_form" : form_send_invoice["email"],
            "wa_telp_form" : form_send_invoice["no_wa"],
            "email_check_form" : form_send_invoice["email_check"],
            "wa_check_form" : form_send_invoice["whatsapp_check"],
            "file_form" : form_send_invoice["invoice"],
            "text_form" : form_send_invoice["message"],
        }
            
        return render(request, self.template_name, context)
    
    def post(self, request, id):
        values = Invoice.objects.select_related("client").get(id=id)
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if is_ajax:
            send_form = SendInvoiceForm(request.POST, request.FILES)
            
            if send_form.is_valid():
                if request.POST["email_check"] == "on":
                    
                    mail_to = send_form.cleaned_data["email"]
                    message = send_form.cleaned_data["message"]
                    attachment = request.FILES["invoice"]
                    
                    email = EmailMessage(
                        subject=f"Here’s your invoice # {values.invoice_num}",
                        body=message,
                        from_email="mch.ardians.dev@gmail.com",
                        to=[mail_to],
                    )
                    
                    email.attach(attachment.name, attachment.read(), attachment.content_type)
                    email.send()
                    
                    values.status = "Active"
                    values.save()
                    
                    return JsonResponse({'message': 'Congratulations! your invoice has been sent'})
            else:
                return JsonResponse({'errors': {**send_form.errors}}, status=400)
    
class InvoiceHistoryViews(View):
    template_name = ""
    
    def get(self, request, id=None):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        query = Invoice.objects.annotate(
        client_name=F('client__nama'),
        ).values(
            'id',
            'client_name',
            'invoice_num',
            'invoice_date', 
            'status'
        ).filter(status="Done")
        
        if is_ajax:
            search_value = request.GET.get('search[value]')
            if search_value:
                query = query.filter(nama__icontains=search_value)

            start = int(request.GET.get('start', 0))
            length = int(request.GET.get('length', 10))
            page_data = query[start:start+length]

            data = []
            for invoice in page_data:
                product_name = list(ClientsProduct.objects.filter(invoice=invoice["id"]).values_list('product__nama_product', flat=True))
                products = ', '.join(product_name)
                
                data.append({
                    'DT_RowIndex': start + 1,
                    'nama': invoice["client_name"],
                    'product': products,
                    'invoice_date': invoice["invoice_date"],
                    'no_invoice': invoice["invoice_num"],
                    'status': invoice["status"],
                    'action': f"""
                                    <div class="dropdown position-relative">
                                        <button class="btn btn-outline border border-0" data-bs-toggle="dropdown" data-bs-display="static">
                                            <i class="align-middle" data-feather="more-vertical"></i>
                                        </button>
                                        <div class="dropdown-menu dropdown-menu-end">
                                            <button class="dropdown-item" id="btn_detail" value="{ invoice["id"] }">Detail</button>
                                        </div>
                                    </div>
                              """
                })
                start += 1
                
            return JsonResponse({
                'draw': int(request.GET.get('draw', 1)),
                'recordsTotal': query.count(),
                'recordsFiltered': query.count(),
                'data': data,
            }) 
            
        return render(request, self.template_name, {"title": "History"})
    
class InvoiceHistoryDetailViews(View):
    template_name = ""
    
    def get(self, request, id):
        client_queryset = Invoice.objects.filter(id=id).select_related("client").get()
        client_product_queryset = ClientsProduct.objects.filter(invoice=id).select_related("product").annotate(result=ExpressionWrapper(F('price') * F('quantity'), output_field=IntegerField()))
        queryset_totals = ClientsProduct.objects.filter(invoice=id).aggregate(total_quantity=Sum('quantity'), total_subtotal=Sum(ExpressionWrapper(F('price') * F('quantity'), output_field=IntegerField())))
        queryset_payment = Invoice.objects.select_related("clientspayment").filter(Q(status="Done")).get(id=id)
            
        client_values = {
            "nama_client" : client_queryset.client.nama,
            "date" : client_queryset.invoice_date,
            "email" : client_queryset.client.email,
            "sub_total" : queryset_totals["total_subtotal"]
        }
        
        detail_form = DetailInvoiceForm(initial=client_values)
        payment_form = PaymentForm(initial={"payment_date": client_queryset.due_date})
            
        context = {
            "title" : "Invoice",
            "no_invoice" : client_queryset.invoice_num,
            "nama_client_form" : detail_form["nama_client"],
            "date_form" : detail_form["date"],
            "email_form" : detail_form["email"],
            "subtotal_form" : detail_form["sub_total"],
            "payment_date_form" : payment_form["payment_date"],
            "payment_report_form" : payment_form["payment_report"],
            "id" : id,
            "list_views" : client_product_queryset,
            "total_quantity" : queryset_totals["total_quantity"],
            "total_subtotal" : queryset_totals["total_subtotal"],
            "file" : queryset_payment,
            "placeholder": os.path.basename(queryset_payment.clientspayment.payment_receipt.url)
        }
            
        return render(request, self.template_name, context)   
    
class InvoiceDetailViews(View):
    template_name = ""
    
    def get(self, request, id):
        client_queryset = Invoice.objects.filter(id=id).select_related("client").get()
        client_product_queryset = ClientsProduct.objects.filter(invoice=id).select_related("product").annotate(result=ExpressionWrapper(F('price') * F('quantity'), output_field=IntegerField()))
        queryset_totals = ClientsProduct.objects.filter(invoice=id).aggregate(total_quantity=Sum('quantity'), total_subtotal=Sum(ExpressionWrapper(F('price') * F('quantity'), output_field=IntegerField())))
        
        client_values = {
            "nama_client" : client_queryset.client.nama,
            "date" : client_queryset.invoice_date,
            "email" : client_queryset.client.email,
            "sub_total" : queryset_totals["total_subtotal"]
        }
        
        detail_form = DetailInvoiceForm(initial=client_values)
        payment_form = PaymentForm(initial={"payment_date": client_queryset.due_date})
        
        context = {
            "title" : "Invoice",
            "no_invoice" : client_queryset.invoice_num,
            "nama_client_form" : detail_form["nama_client"],
            "date_form" : detail_form["date"],
            "email_form" : detail_form["email"],
            "subtotal_form" : detail_form["sub_total"],
            "payment_date_form" : payment_form["payment_date"],
            "payment_report_form" : payment_form["payment_report"],
            "id" : id,
            "list_views" : client_product_queryset,
            "total_quantity" : queryset_totals["total_quantity"],
            "total_subtotal" : queryset_totals["total_subtotal"],
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request, id):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        values = Invoice.objects.filter(id=id).select_related("client").get()
        
        if is_ajax:
            payment_form = PaymentForm(request.POST, request.FILES)
            
            print(request.POST)
            print(request.FILES)
            
            if payment_form.is_valid():
                ClientsPayment.objects.create(
                    no_invoice = values.invoice_num,
                    payment_date = payment_form.cleaned_data["payment_date"],
                    payment_receipt = payment_form.cleaned_data["payment_report"],
                    invoice = values,
                )
                
                values.status = "Done"
                values.save()
                
                return JsonResponse({"message": "Congratulations! confirmation success!"})
            else:
                return JsonResponse({'errors': {**payment_form.errors}}, status=400)
                
                