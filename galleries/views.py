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
            # new_media = form.save(commit=False)
            # new_media.owner = request.user
            # new_media.save()
            
            # form.save_m2m()
            # recent_album = Album.objects.filter(owner=request.user).get(title='Recent')
            # new_media.albums.add(recent_album)
            title=form.cleaned_data['title']
            artist=form.cleaned_data['artist']
            tags=form.cleaned_data['tags']
            albums=form.cleaned_data['albums']
            for media in request.FILES.getlist('file'):
                new_media = MediaUpload(file=media, title=title, artist=artist, tags=tags, owner=request.user)
                new_media.save()
                
                for album in albums:
                    new_media.albums.add(album)
                recent_album = Album.objects.filter(owner=request.user).get(title='Recent')
                new_media.albums.add(recent_album)
            
            return HttpResponseRedirect(reverse('gallery', kwargs={'username':request.user.username}))
    else:
        form = MediaUploadForm(request.user)
    
    context = {'form' : form}
    return render(request, 'galleries/new_media.html', context)

@login_required
def new_album_view(request):
    if request.method == 'POST':
        form = AlbumForm(request.user, request.POST)
        if form.is_valid():
            new_album = form.save(commit=False)
            new_album.owner = request.user
            new_album.save()
            
            return HttpResponseRedirect(reverse('gallery', kwargs={'username':request.user.username}))
    else:
        form = AlbumForm(request.user)
    
    context = {'form' : form}
    return render(request, 'galleries/new_album.html', context)

def gallery_view(request, username):
    owner = User.objects.get(username=username)
    
    albums = Album.objects.filter(owner=owner.pk).order_by('-published_date')
    
    context = {'owner' : owner, 'albums' : albums}
    return render(request, 'galleries/gallery.html', context)

def album_view(request, username, album_title):
    owner = User.objects.get(username=username)
    
    album = Album.objects.get(title=album_title, owner=owner.pk)
    medias = album.mediaupload_set.order_by('-published_date')
    
    context = {'owner' : owner, 'album' : album, 'medias' : medias}
    return render(request, 'galleries/album.html', context)

def media_view(request, username, media_id):
    media = MediaUpload.objects.get(id=media_id)
    
    context = {'media' : media}
    return render(request, 'galleries/media.html', context)
