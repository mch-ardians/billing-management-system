from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views import View
from .models import Client, Alamat
from .forms import FormClient, FormAlamat
import json

# Create your views here.
class ClientViews(View):
    template_name = ""
    
    def get(self, request, id=None):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        query = Client.objects.select_related("alamat").all()
        
        if is_ajax:
            search_value = request.GET.get('search[value]')
            if search_value:
                query = query.filter(nama__icontains=search_value)

            start = int(request.GET.get('start', 0))
            length = int(request.GET.get('length', 10))
            page_data = query[start:start+length]

            data = []
            for client in page_data:
                data.append({
                    'DT_RowIndex': start + 1,
                    'nama': client.nama,
                    'alamat': client.alamat.jalan,
                    'kode_pos': client.alamat.kode_pos,
                    'email': client.email,
                    'no_telp': client.no_wa,
                    'action': f"""
                                    <div class="dropdown position-relative">
                                        <button class="btn btn-outline border border-0" data-bs-toggle="dropdown" data-bs-display="static">
                                            <i class="align-middle" data-feather="more-vertical"></i>
                                        </button>
                                        <div class="dropdown-menu dropdown-menu-end">
                                            <button class="dropdown-item btn-delete" value="{ client.id }" style="color: #1e8a97;">Delete</button>
                                            <button class="dropdown-item btn-edit" value="{ client.id }">Edit</button>
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
            values = Client.objects.select_related("alamat").get(id=id)
            
            client_values = {
                "nama": values.nama,
                "email": values.email,
                "no_wa": values.no_wa,
            }
            
            alamat_values = {
                "jalan": values.alamat.jalan,
                "provinsi": values.alamat.provinsi,
                "kota_kab": values.alamat.kota_kab,
                "kode_pos": values.alamat.kode_pos,
            }
            
            form_client = FormClient(initial=client_values)
            form_alamat = FormAlamat(initial=alamat_values)
            
            context = {
                "title": "Client",
                "client_nama_form": form_client["nama"],
                "alamat_form": form_alamat,
                "client_email_form": form_client["email"],
                "client_wa_form": form_client["no_wa"],
            }
            
            return render(request, self.template_name, context)
        
        form_client = FormClient()
        form_alamat = FormAlamat()
        
        context = {
            "title": "Client",
            "client_nama_form": form_client["nama"],
            "alamat_form": form_alamat,
            "client_email_form": form_client["email"],
            "client_wa_form": form_client["no_wa"],
        }
          
        return render(request, self.template_name, context)

    
    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if is_ajax:
            data = json.loads(request.body.decode('utf-8')) if request.body else {}
            payload = data.get('payload', {})
            
            form_client = FormClient(payload)
            form_alamat = FormAlamat(payload)
            
            if form_client.is_valid() and form_alamat.is_valid():
                client = Client.objects.create(
                    nama = form_client.cleaned_data['nama'], 
                    no_wa = form_client.cleaned_data['no_wa'],
                    email = form_client.cleaned_data['email']
                )
                
                Alamat.objects.create(
                    provinsi = form_alamat.cleaned_data['provinsi'],
                    kota_kab = form_alamat.cleaned_data['kota_kab'],
                    jalan = form_alamat.cleaned_data['jalan'],
                    kode_pos = form_alamat.cleaned_data['kode_pos'],
                    client = client
                )
                
                return JsonResponse({'message': 'Congratulations! Your client has been added!'})
            else:
                return JsonResponse({'errors': {**form_client.errors, **form_alamat.errors}}, status=400)
    
    def put(self, request, id):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        values = Client.objects.select_related("alamat").get(id=id)
        
        if is_ajax:
            data = json.loads(request.body.decode('utf-8')) if request.body else {}
            payload = data.get('payload', {})
            
            form_client = FormClient(payload)
            form_alamat = FormAlamat(payload)
            
            if form_client.is_valid() and form_alamat.is_valid():
                values.nama = form_client.cleaned_data['nama']
                values.email = form_client.cleaned_data['email']
                values.no_wa = form_client.cleaned_data['no_wa']
                values.save()
                
                values.alamat.jalan = form_alamat.cleaned_data['jalan']
                values.alamat.kota_kab = form_alamat.cleaned_data['kota_kab']
                values.alamat.provinsi = form_alamat.cleaned_data['provinsi']
                values.alamat.kode_pos = form_alamat.cleaned_data['kode_pos']
                values.alamat.save()
                
                return JsonResponse({'message': 'Congratulations! Your client has been changed!'})
    
    def delete(self, request, id):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if is_ajax:
            get_object_or_404(Client, id=id).delete()
            return JsonResponse({'message': 'Congratulations! Your client has been deleted!'})