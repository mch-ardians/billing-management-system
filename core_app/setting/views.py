from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from product.models import Product
from django.core.management import call_command
from .forms import FormSetting
from .models import Setting
import json

# Create your views here.
class SettingViews(View):
    template_name = ""
    
    def get(self, request, id=None):
        if id:
            notifications = Setting.objects.select_related("product").get(id=id)
            
            notif_values = {
                "notif_date": notifications.notif_date,
                "notif_time": notifications.notif_time,
                "client": notifications.client,
                "product": notifications.product,
                "notif_text": notifications.text,
            }
            
            if notifications.email:
                notif_values["checkbox_email"] = True
                notif_values["email_check"] = notifications.email
            
            if eval(notifications.status) == True:
                notif_values["repeat_notif"] = True
                notif_values["status"] = True
            
            setting_form = FormSetting(initial=notif_values)
            
            context = {
                "title": "Setting",
                "notif_date_form": setting_form["notif_date"],
                "notif_time_form": setting_form["notif_time"],
                "client_form": setting_form["client"],
                "product_form": setting_form["product"],
                "text_form": setting_form["notif_text"],
                "checkbox_telp_form": setting_form["checkbox_telp"],
                "telp_check_form": setting_form["telp_check"],
                "checkbox_email_form": setting_form["checkbox_email"],
                "email_check_form": setting_form["email_check"],
                "repeat_notif_form": setting_form["repeat_notif"],
                "status_form": setting_form["status"],
            }
        
            return render(request, self.template_name, context)
        
        notifications = Setting.objects.all()
        setting_form = FormSetting()
        
        context = {
            "title": "Setting",
            "notif_date_form": setting_form["notif_date"],
            "notif_time_form": setting_form["notif_time"],
            "client_form": setting_form["client"],
            "product_form": setting_form["product"],
            "text_form": setting_form["notif_text"],
            "checkbox_telp_form": setting_form["checkbox_telp"],
            "telp_check_form": setting_form["telp_check"],
            "checkbox_email_form": setting_form["checkbox_email"],
            "email_check_form": setting_form["email_check"],
            "repeat_notif_form": setting_form["repeat_notif"],
            "status_form": setting_form["status"],
            "notif": notifications
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if is_ajax:
            data = json.loads(request.body.decode('utf-8')) if request.body else {}
            payload = data.get('payload', {})
            
            form_setting = FormSetting(payload)
            
            if form_setting.is_valid():
                values = Setting.objects.create(
                    notif_date = form_setting.cleaned_data["notif_date"],
                    notif_time = form_setting.cleaned_data["notif_time"],
                    client = form_setting.cleaned_data["client"],
                    product = form_setting.cleaned_data["product"],
                    text = form_setting.cleaned_data["notif_text"],
                    email = form_setting.cleaned_data["email_check"],
                    status = form_setting.cleaned_data["status"]
                )
                
                if eval(str(values.status)) == True:
                    call_command('crontab', 'add')
                    return JsonResponse({"message": "Setting notification is complete"})
                
                return JsonResponse({"message": "Setting notification is complete"})
            else:
                return JsonResponse({'errors': {**form_setting.errors}}, status=400)
    
    def put(self, request, id):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        values = Setting.objects.get(id=id)
        
        if is_ajax:
            data = json.loads(request.body.decode('utf-8')) if request.body else {}
            payload = data.get('payload', {})

            if len(payload) == 2:
                values.status = payload["status"]
                values.save()
                
                if eval(values.status) == True:
                    call_command('crontab', 'add')
                    return JsonResponse({"message": "Successfully activated scheduled email!"})
                else:
                    setting_count = Setting.objects.filter(status='True').count()

                    if setting_count >= 1:
                        return JsonResponse({"message": "Successfully disabled scheduled email"})
                    else:
                        call_command('crontab', 'remove')
                        return JsonResponse({"message": "Successfully disabled scheduled email"})
            
            form_setting = FormSetting(payload)
            
            if form_setting.is_valid():
                values.notif_date = form_setting.cleaned_data["notif_date"]
                values.notif_time = form_setting.cleaned_data["notif_time"]
                values.client = form_setting.cleaned_data["client"]
                values.product = form_setting.cleaned_data["product"]
                values.text = form_setting.cleaned_data["notif_text"]
                values.email = form_setting.cleaned_data["email_check"]
                values.status = form_setting.cleaned_data["status"]
                values.save()
                
                if eval(str(values.status)) == True:
                    call_command('crontab', 'add')
                    return JsonResponse({"message": "Update notification setting is complete"})
                else:
                    setting_count = Setting.objects.filter(status='True').count()
                    
                    if setting_count >= 1:
                        return JsonResponse({"message": "Successfully disabled scheduled email"})
                    else:
                        call_command('crontab', 'remove')
                        return JsonResponse({"message": "Successfully disabled scheduled email"})

class SettingProductViews(View):
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