from django.shortcuts import get_object_or_404, render
from setting.models import Setting
from django.views import View
from django.http import JsonResponse
from datetime import date

# Create your views here.
class DashboardViews(View):
    template_name = ""
    
    def get(self, request):
        today = date.today()
        
        notif_today = Setting.objects.filter(notif_date=today)
        notif_upcoming = Setting.objects.filter(notif_date__gt=today)
        
        context = {
            'notif_today': notif_today,
            'notif_upcoming': notif_upcoming,
            'title': 'dashboard'
        }
        
        return render(request, self.template_name, context)
    
    def delete(self, request,id):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if is_ajax:
            get_object_or_404(Setting, id=id).delete()
            
            return JsonResponse({'message': 'Congratulations! Your notification has been marked as done!'})