from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

def galleries_view(request):
    registered_users = User.objects.all()
    context = {'registered_users' : registered_users}
    return render(request, 'galleries/index.html', context)

@login_required
def new_media_view(request):
    if request.method == 'POST':
        form = MediaUploadForm(request.user ,request.POST, request.FILES)
        if form.is_valid():
            new_media = form.save(commit=False)
            new_media.owner = request.user
            new_media.save()
            form.save_m2m()
            
            return HttpResponseRedirect(reverse('gallery', kwargs={'username':request.user.username}))
    else:
        form = MediaUploadForm(request.user)
    
    context = {'form' : form}
    return render(request, 'galleries/new_media.html', context)

@login_required
def new_album_view(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            new_album = form.save(commit=False)
            new_album.owner = request.user
            new_album.save()
            
            return HttpResponseRedirect(reverse('albums', kwargs={'username':request.user.username}))
    else:
        form = AlbumForm()
    
    context = {'form' : form}
    return render(request, 'galleries/new_album.html', context)

def gallery_view(request, username):
    print(username)
    owner = User.objects.get(username=username)
    
    albums = Album.objects.filter(owner=owner.pk).order_by('-published_date')
    medias = MediaUpload.objects.filter(owner=owner.pk).order_by('-published_date')
    
    context = {'owner' : owner, 'albums' : albums, 'medias' : medias}
    return render(request, 'galleries/gallery.html', context)

def albums_view(request, username):
    owner = User.objects.get(username=username)
    
    albums = Album.objects.filter(owner=owner.pk).order_by('-published_date')

    context = {'owner':owner, 'albums' : albums}
    return render(request, 'galleries/albums.html', context)

def album_view(request, username, album_id):
    owner = User.objects.get(username=username)
    
    album = Album.objects.get(id=album_id)
    medias = album.mediaupload_set.order_by('-published_date')
    
    context = {'owner' : owner, 'album' : album, 'medias' : medias}
    return render(request, 'galleries/album.html', context)

def media_view(request, username, media_id):
    media = MediaUpload.objects.get(id=media_id)
    
    context = {'media' : media}
    return render(request, 'galleries/media.html', context)
