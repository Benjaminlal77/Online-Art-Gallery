from django.urls import path

from . import views

urlpatterns = [
    path('', views.galleries_view, name='galleries'),
    path('new_media/', views.new_media_view, name='new_media'),
    path('new_album/', views.new_album_view, name='new_album'),
    path('<username>/', views.gallery_view, name='gallery'),

    path('<username>/albums/', views.albums_view, name='albums'),
    path('<username>/albums/<album_id>/', views.album_view, name='album'),    
    path('<username>/<media_id>/', views.media_view, name='media'),
] 
