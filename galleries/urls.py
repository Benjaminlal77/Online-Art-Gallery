from os import name
from django.urls import path

from . import views

urlpatterns = [
    path('', views.galleries_view, name='galleries'),
    
    path('my_gallery/', views.my_gallery_view, name='my_gallery'),
    path('my_gallery/albums/', views.albums_view, name='albums'),
    path('my_gallery/albums/new_album/', views.new_album_view, name='new_album'),
    path('my_gallery/albums/<album_id>/', views.album_view, name='album'),    
    path('my_gallery/new_media/', views.new_media_view, name='new_media'),
    path('my_gallery/<media_id>/', views.media_view, name='media'),
] 
