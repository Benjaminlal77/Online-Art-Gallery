from django.http.response import Http404
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

import math

def check_if_page_exists(page, page_num):
    if page_num > page.num_of_pages or page_num < 1:
        raise Http404

class Page:
    def __init__(self, objects, current_page_num, num_of_objects_per_page):
        self.previous_page_num = current_page_num - 1
        self.current_page_num = current_page_num
        self.next_page_num = current_page_num + 1
        
        self.num_of_pages = math.ceil(len(objects)/num_of_objects_per_page)
        if not self.num_of_pages:
            self.num_of_pages = 1
            
        self.is_not_first_page = current_page_num != 1
        self.is_not_last_page = current_page_num != self.num_of_pages

def search_view(request, page_num):
    def get_main_page():
        page_checked_before = pages_to_check[0]
        page = page_checked_before
        for page_to_check in pages_to_check:
            if page_to_check.num_of_pages > page_checked_before.num_of_pages:
                page = page_to_check
            page_checked_before = page_to_check
        
        return page
    
    def search_for_objects():
        print(request.GET)
        if 'albums-checkbox' in request.GET:
            albums_page = Page(Album.objects.filter(title__icontains=query), page_num, 9)
            pages_to_check.append(albums_page)
            context['searched_for_albums'] = True
        
        if 'users-checkbox' in request.GET:
            users_page = Page(User.objects.filter(username__icontains=query), page_num, 20)
            pages_to_check.append(users_page)
            context['searched_for_users'] = True
            
        if 'medias-checkbox' in request.GET or len(context) == 0:
            medias_page = Page(MediaUpload.objects.filter(tags__icontains=query), page_num, 20)
            pages_to_check.append(medias_page)
            context['searched_for_medias'] = True
        
    def get_objects():
        if 'searched_for_albums' in context:
            starting_index = (page_num * 9) - 9
            ending_index = starting_index + 9
    
            albums = Album.objects.filter(title__icontains=query).order_by('-published_date').reverse()[starting_index:ending_index]
            context['albums'] = albums
        
        if 'searched_for_users' in context:
            starting_index = (page_num * 20) - 20
            ending_index = starting_index + 20
    
            users = User.objects.filter(username__icontains=query).order_by('-date_joined').reverse()[starting_index:ending_index]
            context['registered_users'] = users
        
        if 'searched_for_medias' in context:
            starting_index = (page_num * 20) - 20
            ending_index = starting_index + 20
    
            medias = MediaUpload.objects.filter(tags__icontains=query).order_by('-published_date').reverse()[starting_index:ending_index]
            context['medias'] = medias
    
    if 'q' in request.GET:            
        query = request.GET['q']
        context = {}
        pages_to_check = []
        
        search_for_objects()
        page = get_main_page()
        
        check_if_page_exists(page, page_num)
        get_objects()
        
    else:
        query = ''
        
        page = Page(MediaUpload.objects.all(), page_num, 20)
        check_if_page_exists(page, page_num)
        
        starting_index = (page_num * 20) - 20
        ending_index = starting_index + 20
        
        medias = MediaUpload.objects.all()[starting_index:ending_index]
        context = {'medias' : medias, 'searched_for_medias' : True}
    
    context['page'] = page
    context['query'] = query
    return render(request, 'galleries/search.html', context)

@login_required
def new_media_view(request):
    if request.method == 'POST':
        form = MediaUploadForm(request.user ,request.POST, request.FILES)
        if form.is_valid():
            title=form.cleaned_data['title']
            artist=form.cleaned_data['artist']
            tags=form.cleaned_data['tags']
            albums=form.cleaned_data['albums']
            
            if title == '':
                title = 'Untitled'
            if artist == '':
                artist = 'Unknown'
            tags = [tag for tag in tags.split(',')]
            
            for media in request.FILES.getlist('file'):
                new_media = MediaUpload(file=media, title=title, artist=artist, tags=tags, owner=request.user)
                new_media.save()
                
                for album in albums:
                    new_media.albums.add(album)
                recent_album = Album.objects.filter(owner=request.user).get(title='Recent')
                new_media.albums.add(recent_album)
            
            return HttpResponseRedirect(reverse('gallery', kwargs={'username':request.user.username,'page_num':1}))
    else:
        form = MediaUploadForm(request.user)
    
    context = {'form' : form}
    return render(request, 'galleries/new_media.html', context)

@login_required
def new_album_view(request):
    if request.method == 'POST':
        form = AlbumForm(request.user, request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            
            new_album = form.save(commit=False)
            new_album.owner = request.user
            new_album.save()
            
            return HttpResponseRedirect(reverse('gallery', kwargs={'username':request.user.username, 'page_num':1}))
    else:
        form = AlbumForm(request.user)
    
    context = {'form' : form}
    return render(request, 'galleries/new_album.html', context)

def gallery_view(request, username, page_num):
    owner = User.objects.get(username=username)
    
    albums = Album.objects.filter(owner=owner.pk)
    page = Page(albums, page_num, 9)
    
    check_if_page_exists(page, page_num)
    
    starting_index = (page_num * 9) - 9
    ending_index = starting_index + 9
    
    albums = Album.objects.filter(owner=owner.pk).order_by('-published_date').reverse()[starting_index:ending_index]
    
    context = {'owner' : owner, 'albums' : albums, 'page' : page}
    return render(request, 'galleries/gallery.html', context)

def album_view(request, username, album_title, page_num):
    owner = User.objects.get(username=username)
    
    album = Album.objects.get(title=album_title, owner=owner.pk)
    medias = album.mediaupload_set.order_by('-published_date')
    page = Page(medias, page_num, 20)
    
    check_if_page_exists(page, page_num)

    starting_index = (page_num * 20) - 20
    ending_index = starting_index + 20
    medias = album.mediaupload_set.order_by('-published_date')[starting_index:ending_index]
    
    context = {'owner' : owner, 'album' : album, 'medias' : medias, 'page' : page}
    return render(request, 'galleries/album.html', context)

def media_view(request, username, media_id): 
    media = MediaUpload.objects.get(id=media_id)
    
    context = {'media' : media}
    return render(request, 'galleries/media.html', context)

def delete_album(request, username, album_title):
    if request.method == 'POST':
        owner = User.objects.get(username=username)
        Album.objects.filter(owner=owner.pk).get(title=album_title).delete()
        
    return HttpResponseRedirect(reverse('gallery', kwargs={'username':request.user.username, 'page_num': 1}))

def delete_media(request, username, media_id):
    if request.method == 'POST':
        MediaUpload.objects.get(id=media_id).delete()
        
    return HttpResponseRedirect(reverse('gallery', kwargs={'username':request.user.username, 'page_num' : 1}))
