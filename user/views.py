from rest_framework import viewsets,status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse     
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from grunge.models import Album, Artist, Track
from grunge.serializers import ArtistSerializer
from django.views import View
from utils import call_http

class Login(View):                        
    def get(self, request):      
            return render(request, "user/login.html")

    def post(self,request):
        try:
            username = request.POST.get('username',None)
            password = request.POST.get('password',None)
            errorList = {}

            if username is None or not username:
                errorList['username'] = 'User Name is required field'

            if password is None or not password:
                errorList['password'] = 'Password is required field'

            
            if len(errorList) != 0:
                return JsonResponse({'status_code':400,'msg':'Something missing','errorList':errorList})
        
            user = authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                return JsonResponse({'status_code':200,'msg':'Login succesfully succesfully'})
            else:
                return JsonResponse({'status_code':400,'msg':'Invalid credential'})
           
        except Exception as e: 
            return JsonResponse({'status_code':500,'msg':str(e)})

class Logout(View):
    def get(self, request):
        user = request.user
        if user:
            logout(request)
            return redirect('/user/login')

class Artists(View):                        
    def get(self, request): 
        user = request.user
        if not user.is_authenticated:
            return redirect('/user/login')
        page = 1
        prev_page = int(page)
        if 'page' in request.GET:
            page = int(request.GET.get('page'))
        if page > 1:
            prev_page = page - 1
        response = call_http(api_name=f'artists?page={page}',method_type='get')
        if 'detail' in response:
            if response['detail'] == 'Invalid page.':
                response['results'] = []
                next_page = page
        else:
            next_page = int(page) + 1
        template_data = {}
        template_data['results'] = response['results']
        template_data['prev_page'] = prev_page
        template_data['next_page'] = next_page
        return render(request, "user/artist/list.html",template_data)

    def post(self, request): 
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'status_code':400,'msg':'Invalid login credential'})
        try:
            uuid = request.POST.get('uuid',None)
            name = request.POST.get('name',None)
            if name is None or  name == '':
                return JsonResponse({'status_code':400,'msg':'Please enter artist name'})
            data = {'name':name}
            msg = ''
            response = None
            if uuid is None or uuid == '':
                msg = 'Artist created'
                response = call_http(api_name='artists',method_type='post',data=data)
                print(response)
            else:
                msg = 'Artist updated'
                response = call_http(api_name=f'artists/{uuid}',method_type='put',data=data)

            if 'uuid' not in response:
                return JsonResponse({'status_code':400,'msg':'Something error'})
            messages.success(request, msg)
            return JsonResponse({'status_code':200,'msg':msg})
        except:
            return JsonResponse({'status_code':500,'msg':'Server error'})
    
    def delete(self, request, *args, **kwargs): 
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'status_code':400,'msg':'Invalid login credential'})
        try:
            uuid = kwargs['uuid']
            msg = 'Artist deleted'
            response = call_http(api_name=f'artists/{uuid}',method_type='delete')
            if 'uuid' not in response:
                return JsonResponse({'status_code':400,'msg':'Something error'})
            messages.success(request, msg)
            return JsonResponse({'status_code':200,'msg':msg})
        except:
            return JsonResponse({'status_code':500,'msg':'Server error'})
    
    def get_artist_info(request,*args,**kwargs):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'status':400,'msg':'Invalid login credential'})
        uuid = kwargs['uuid']
        artist_info = call_http(api_name=f'artists/{uuid}',method_type='get')
        return JsonResponse({'status_code':200,'artist_info':artist_info})


class Albums(View):                        
    def get(self, request): 
        user = request.user
        if not user.is_authenticated:
            return redirect('/user/login')
        page = 1
        prev_page = int(page)
        if 'page' in request.GET:
            page = int(request.GET.get('page'))
        if page > 1:
            prev_page = page - 1
        response = call_http(api_name=f'albums?page={page}',method_type='get')
        artists = Artist.objects.all().order_by('name')
        artist_list = []
        for a in artists:
            artist_list.append({'uuid':a.uuid,'name':a.name})
        if 'detail' in response:
            if response['detail'] == 'Invalid page.':
                response['results'] = []
                next_page = page
        else:
            next_page = int(page) + 1
    
        template_data = {}
        template_data['results'] = response['results']
        template_data['prev_page'] = prev_page
        template_data['next_page'] = next_page
        template_data['artist_list'] = artist_list
        return render(request, "user/album/list.html",template_data)
    
    def post(self, request): 
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'status_code':400,'msg':'Invalid login credential'})
        try:
            uuid = request.POST.get('uuid',None)
            name = request.POST.get('name',None)
            year = request.POST.get('year',None)
            artist = request.POST.get('artist',None)
            tracks = request.POST.getlist('tracks[]',[])
            track_numbers = request.POST.getlist('track_numbers[]',[])
            errors = {}

            if name is None or  name == '':
                errors['name'] = "Please enter album name"
            if year is None or  year == '':
                errors['year'] = "Please enter year"
            if artist is None or  artist == '':
                errors['artist'] = "Please select artist"
            
            if len(errors) > 0:
                return JsonResponse({'status_code':400,'msg':'Missing some field information','errors':errors})
            artist_obj = Artist.objects.filter(uuid=artist).first()
            artist_info = {}
            artist_info['id'] = artist_obj.id
            artist_info['name'] = artist_obj.name
            i = 0
            track_list = []
            for track in tracks:
                track_list.append({"name":track,"number":track_numbers[i]})
                i += 1
            data = {}
            data['name'] = name
            data['year'] = year
            data['artist'] = artist_info
            data['tracks'] = track_list
            msg = ''
            response = None
            if uuid is None or uuid == '':
                msg = 'Album created'
                response = call_http(api_name='albums',method_type='post',data=data)
            else:
                msg = 'Album updated'
                response = call_http(api_name=f'albums/{uuid}',method_type='put',data=data)
            if 'uuid' not in response:
                return JsonResponse({'status_code':400,'msg':'Something error'})
            messages.success(request, msg)
            return JsonResponse({'status_code':200,'msg':msg})
        except:
            return JsonResponse({'status_code':500,'msg':'Server error'})
    
    def delete(self, request, *args, **kwargs): 
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'status_code':400,'msg':'Invalid login credential'})
        try:
            uuid = kwargs['uuid']
            msg = 'Album deleted'
            response = call_http(api_name=f'albums/{uuid}',method_type='delete')
            if 'uuid' not in response:
                return JsonResponse({'status_code':400,'msg':'Something error'})
            messages.success(request, msg)
            return JsonResponse({'status_code':200,'msg':msg})
        except:
            return JsonResponse({'status_code':500,'msg':'Server error'})

    def get_album_info(request,*args,**kwargs):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'status':400,'msg':'Invalid login credential'})
        uuid = kwargs['uuid']
        album_info = call_http(api_name=f'albums/{uuid}',method_type='get')
        return JsonResponse({'status_code':200,'album_info':album_info})


class Tracks(View):                        
    def get(self, request): 
        user = request.user
        if not user.is_authenticated:
            return redirect('/user/login')
        page = 1
        prev_page = int(page)
        if 'page' in request.GET:
            page = int(request.GET.get('page'))
        if page > 1:
            prev_page = page - 1
        response = call_http(api_name=f'tracks?page={page}',method_type='get')
        albums = Album.objects.all().order_by('name')
        album_list = []
        for a in albums:
            album_list.append({'uuid':a.uuid,'name':a.name})
        if 'detail' in response:
            if response['detail'] == 'Invalid page.':
                response['results'] = []
                next_page = page
        else:
            next_page = int(page) + 1
    
        template_data = {}
        template_data['results'] = response['results']
        template_data['prev_page'] = prev_page
        template_data['next_page'] = next_page
        template_data['album_list'] = album_list
        return render(request, "user/track/list.html",template_data)
    
    def post(self, request): 
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'status_code':400,'msg':'Invalid login credential'})
        try:
            uuid = request.POST.get('uuid',None)
            name = request.POST.get('name',None)
            number = request.POST.get('number',None)
            album = request.POST.get('album',None)
            errors = {}

            if name is None or  name == '':
                errors['name'] = "Please enter album name"
            if number is None or  number == '':
                errors['number'] = "Please enter track number"
            if album is None or  album == '':
                errors['album'] = "Please select track album"
            
            if len(errors) > 0:
                return JsonResponse({'status_code':400,'msg':'Missing some field information','errors':errors})
            album_obj = Album.objects.filter(uuid=album).first()
            data = {}
            data['name'] = name
            data['number'] = number
            data['album_id'] = album_obj.id
            msg = ''
            response = None
            if uuid is None or uuid == '':
                msg = 'Track created'
                response = call_http(api_name='tracks',method_type='post',data=data)
            else:
                msg = 'Track updated'
                response = call_http(api_name=f'tracks/{uuid}',method_type='put',data=data)
            if 'uuid' not in response:
                return JsonResponse({'status_code':400,'msg':'Something error'})
            messages.success(request, msg)
            return JsonResponse({'status_code':200,'msg':msg})
        except:
            return JsonResponse({'status_code':500,'msg':'Server error'})
    
    def delete(self, request, *args, **kwargs): 
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'status_code':400,'msg':'Invalid login credential'})
        try:
            uuid = kwargs['uuid']
            msg = 'Track deleted'
            response = call_http(api_name=f'tracks/{uuid}',method_type='delete')
            if 'uuid' not in response:
                return JsonResponse({'status_code':400,'msg':'Something error'})
            messages.success(request, msg)
            return JsonResponse({'status_code':200,'msg':msg})
        except:
            return JsonResponse({'status_code':500,'msg':'Server error'})
        
    def get_track_info(request,*args,**kwargs):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'status':400,'msg':'Invalid login credential'})
        uuid = kwargs['uuid']
        track_info = call_http(api_name=f'tracks/{uuid}',method_type='get')
        return JsonResponse({'status_code':200,'track_info':track_info})
        

class Playlists(View):                        
    def get(self, request): 
        user = request.user
        if not user.is_authenticated:
            return redirect('/user/login')
        page = 1
        prev_page = int(page)
        if 'page' in request.GET:
            page = int(request.GET.get('page'))
        if page > 1:
            prev_page = page - 1
        response = call_http(api_name=f'playlists?page={page}',method_type='get')
        tracks = Track.objects.all().order_by('name')
        track_list = []
        for a in tracks:
            track_list.append({'uuid':a.uuid,'name':a.name})
        if 'detail' in response:
            if response['detail'] == 'Invalid page.':
                response['results'] = []
                next_page = page
        else:
            next_page = int(page) + 1
    
        template_data = {}
        template_data['results'] = response['results']
        template_data['prev_page'] = prev_page
        template_data['next_page'] = next_page
        template_data['track_list'] = track_list
        return render(request, "user/playlist/list.html",template_data)
    
    def post(self, request): 
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'status_code':400,'msg':'Invalid login credential'})
        try:
            uuid = request.POST.get('uuid',None)
            name = request.POST.get('name',None)
            tracks = request.POST.getlist('tracks[]',[])
            errors = {}

            if name is None or  name == '':
                errors['name'] = "Please enter playlist name"
            
            if len(errors) > 0:
                return JsonResponse({'status_code':400,'msg':'Missing some field information','errors':errors})
            tracks = list(set(tracks))
            track_list = []
            for track in tracks:
                track_info = Track.objects.filter(uuid=track).first()
                track_list.append(track_info.id)
            data = {}
            data['name'] = name
            data['tracks'] = track_list
            msg = ''
            response = None
            if uuid is None or uuid == '':
                msg = 'Playlist created'
                response = call_http(api_name='playlists',method_type='post',data=data)
            else:
                msg = 'Playlist updated'
                response = call_http(api_name=f'playlists/{uuid}',method_type='put',data=data)
            if 'uuid' not in response:
                return JsonResponse({'status_code':400,'msg':'Something error'})
            messages.success(request, msg)
            return JsonResponse({'status_code':200,'msg':msg})
        except:
            return JsonResponse({'status_code':500,'msg':'Server error'})
    
    def delete(self, request, *args, **kwargs): 
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'status_code':400,'msg':'Invalid login credential'})
        try:
            uuid = kwargs['uuid']
            msg = 'Album deleted'
            response = call_http(api_name=f'albums/{uuid}',method_type='delete')
            if 'uuid' not in response:
                return JsonResponse({'status_code':400,'msg':'Something error'})
            messages.success(request, msg)
            return JsonResponse({'status_code':200,'msg':msg})
        except:
            return JsonResponse({'status_code':500,'msg':'Server error'})

    def get_playlist_info(request,*args,**kwargs):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'status':400,'msg':'Invalid login credential'})
        uuid = kwargs['uuid']
        playlist_info = call_http(api_name=f'playlists/{uuid}',method_type='get')
        return JsonResponse({'status_code':200,'playlist_info':playlist_info})