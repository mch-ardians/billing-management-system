from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views import View
from .models import Product
from .forms import FormProduct
import json

# Create your views here.
class ProductViews(View):
    template_name = ""
    
    def get(self, request, id=None):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        query = Product.objects.select_related("client").all()
        
        if is_ajax:
            search_value = request.GET.get('search[value]')
            if search_value:
                query = query.filter(nama__icontains=search_value)

            start = int(request.GET.get('start', 0))
            length = int(request.GET.get('length', 10))
            page_data = query[start:start+length]

            data = []
            for product in page_data:
                data.append({
                    'DT_RowIndex': start + 1,
                    'product': product.nama_product,
                    'type': product.type,
                    'client': product.client.nama,
                    'action': f"""
                                    <div class="dropdown position-relative">
                                        <button class="btn btn-outline border border-0" data-bs-toggle="dropdown" data-bs-display="static">
                                            <i class="align-middle" data-feather="more-vertical"></i>
                                        </button>
                                        <div class="dropdown-menu dropdown-menu-end">
                                            <button class="dropdown-item btn-delete" value="{ product.id }" style="color: #1e8a97;">Delete</button>
                                            <button class="dropdown-item btn-edit" value="{ product.id }">Edit</button>
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
        
        if id:  
            values = Product.objects.select_related("client").get(id=id)
            
            product_values = {
                "nama_product": values.nama_product,
                "type": values.type,
                "client": values.client,
            }
            
            form_product = FormProduct(initial=product_values)
            
            context = {
                "title": "Product",
                "product_nama_form": form_product["nama_product"],
                "product_type_form": form_product["type"],
                "product_client_form": form_product["client"],
            }
            
            return render(request, self.template_name, context)
        
        form_product = FormProduct()
        
        context = {
            "title": "Product",
            "product_nama_form": form_product["nama_product"],
            "product_type_form": form_product["type"],
            "product_client_form": form_product["client"],
        }
          
        return render(request, self.template_name, context)
    
    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if is_ajax:
            data = json.loads(request.body.decode('utf-8')) if request.body else {}
            payload = data.get('payload', {})
            
            form_product = FormProduct(payload)
            
            if form_product.is_valid():
                Product.objects.create(
                    nama_product = form_product.cleaned_data['nama_product'], 
                    type = form_product.cleaned_data['type'],
                    client_id = form_product.cleaned_data['client'].id
                )
                
                return JsonResponse({'message': 'Congratulations! Your product has been added!'})
            else:
                return JsonResponse({'errors': {**form_product.errors}}, status=400)
    
    def put(self, request, id):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        values = Product.objects.select_related("client").get(id=id)
        
        if is_ajax:
            data = json.loads(request.body.decode('utf-8')) if request.body else {}
            payload = data.get('payload', {})
            
            form_product = FormProduct(payload)
            
            if form_product.is_valid():
                values.nama_product = form_product.cleaned_data['nama_product']
                values.type = form_product.cleaned_data['type']
                values.client = form_product.cleaned_data['client']
                values.save()
                
                return JsonResponse({'message': 'Congratulations! Your client has been changed!'})
    
    def delete(self, request, id):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if is_ajax:
            get_object_or_404(Product, id=id).delete()
            return JsonResponse({'message': 'Congratulations! Your product has been deleted!'})