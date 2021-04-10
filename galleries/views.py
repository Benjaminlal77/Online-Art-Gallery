from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import *
from .forms import *

def galleries_view(request):
    context = {}
    return render(request, 'galleries/index.html', context)

def my_gallery_view(request):
    albums = Album.objects.all()
    medias = MediaUpload.objects.all()
    
    context = {'medias' : medias, 'albums' : albums}
    return render(request, 'galleries/my_gallery.html', context)

def new_album_view(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            new_album = form.save(commit=False)
            new_album.save()
            return HttpResponseRedirect(reverse('albums'))
    else:
        form = AlbumForm()
    
    context = {'form' : form}
    return render(request, 'galleries/new_album.html', context)

def albums_view(request):
    albums = Album.objects.all()

    context = {'albums' : albums}
    return render(request, 'galleries/albums.html', context)

def album_view(request, album_id):
    album = Album.objects.get(id=album_id)
    medias = album.mediaupload_set.order_by('-published_date')
    
    context = {'album' : album, 'medias' : medias}
    return render(request, 'galleries/album.html', context)

def new_media_view(request):
    if request.method == 'POST':
        form = MediaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('my_gallery'))
    else:
        form = MediaUploadForm()
    
    context = {'form' : form}
    return render(request, 'galleries/new_media.html', context)

def media_view(request, media_id):
    media = MediaUpload.objects.get(id=media_id)
    
    context = {'media' : media}
    return render(request, 'galleries/media.html', context)
