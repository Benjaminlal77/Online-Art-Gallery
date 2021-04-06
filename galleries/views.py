from django.shortcuts import render

from .models import Album, MediaUpload

def galleries_view(request):
    context = {}
    return render(request, 'galleries/index.html', context)

def my_gallery_view(request):
    albums = Album.objects.all()
    medias = MediaUpload.objects.all()
    
    context = {'medias' : medias, 'albums' : albums}
    return render(request, 'galleries/my_gallery.html', context)

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
    return render(request, 'galleries/new_media.html')

def media_view(request, media_id):
    media = MediaUpload.objects.get(id=media_id)
    
    context = {'media' : media}
    return render(request, 'galleries/media.html', context)
