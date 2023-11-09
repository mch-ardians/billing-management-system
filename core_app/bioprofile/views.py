from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.conf import settings
from .forms import ProfileForm
from .models import Profile
import os, io, subprocess
from django.core.management import call_command

# Create your views here.
class ProfileViews(View):
    template_name = ""
    
    def get(self, request, id=None):
        if id:
            values = Profile.objects.select_related("user").get(user_id=id)
            
            profile_values = {
                "username" : values.user.username,
                "full_name" : values.full_name,
                "position" : values.position,
                "email" : values.user.email,
                "no_telp" : values.no_telp_wa
            }
            
            profile_form = ProfileForm(initial=profile_values)
            
            picture_url = ""
        
            if values.foto:
                picture_url = values.foto.url
            else:
                picture_url = '/static/img/avatars/pngwing.com.png'
            
            context = {
                "profile_foto_form" : profile_form["foto"],
                "user_username_form" : profile_form["username"],
                "profile_full_name_form" : profile_form["full_name"],
                "profile_position_form" : profile_form["position"],
                "user_email_form" : profile_form["email"],
                "profile_no_telp_form" : profile_form["no_telp"],
                "foto_profile" : picture_url,
                "title" : "Profile",
            }
            return render(request, "index_profile.html", context)
    
    def post(self, request, id):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if is_ajax:
            profile = Profile.objects.get(user=request.user)
            if request.POST.get('_method') == 'PUT':
                form = ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                if profile.foto and form.cleaned_data["foto"]:
                    old_profile = os.path.join(settings.MEDIA_ROOT, profile.foto.path)
                    if os.path.exists(old_profile):
                        os.remove(old_profile)
                    
                    profile.foto = form.cleaned_data["foto"]
                    profile.user.username = form.cleaned_data["username"]
                    profile.full_name = form.cleaned_data["full_name"]
                    profile.position = form.cleaned_data["position"]
                    profile.user.email = form.cleaned_data["email"]
                    profile.no_telp_wa = form.cleaned_data["no_telp"]
                    profile.save()
                    
                    return JsonResponse({'message': 'Congratulations! Your profile has been changed!'})

                elif profile.foto and not form.cleaned_data["foto"]:
                    profile.foto = profile.foto
                    profile.user.username = form.cleaned_data["username"]
                    profile.full_name = form.cleaned_data["full_name"]
                    profile.position = form.cleaned_data["position"]
                    profile.user.email = form.cleaned_data["email"]
                    profile.no_telp_wa = form.cleaned_data["no_telp"]
                    profile.save()
                    
                    return JsonResponse({'message': 'Congratulations! Your profile has been changed!'})
                
                elif not profile.foto and form.cleaned_data["foto"]:
                    profile.foto = form.cleaned_data["foto"]
                    profile.user.username = form.cleaned_data["username"]
                    profile.full_name = form.cleaned_data["full_name"]
                    profile.position = form.cleaned_data["position"]
                    profile.user.email = form.cleaned_data["email"]
                    profile.no_telp_wa = form.cleaned_data["no_telp"]
                    profile.save()
                    
                    return JsonResponse({'message': 'Congratulations! Your profile has been changed!'})
                
                else:
                    profile.user.username = form.cleaned_data["username"]
                    profile.full_name = form.cleaned_data["full_name"]
                    profile.position = form.cleaned_data["position"]
                    profile.user.email = form.cleaned_data["email"]
                    profile.no_telp_wa = form.cleaned_data["no_telp"]
                    profile.save()
                
                    return JsonResponse({'message': 'Congratulations! Your profile has been changed!'})
            else:
                return JsonResponse({'errors': {**form.errors}}, status=400)
    
    def delete(self, request, id):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if is_ajax:
            profile = Profile.objects.get(user=request.user)
            if profile.foto:
                foto_path = os.path.join(settings.MEDIA_ROOT, profile.foto.path)
                if os.path.exists(foto_path):
                    os.remove(foto_path)
                    profile.foto.delete()
                    
                    return JsonResponse({'message': 'Congratulations! Your profile has been deleted!'})