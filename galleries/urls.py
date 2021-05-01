from django.urls import path

from . import views

urlpatterns = [
    path('', views.galleries_view, name='galleries'),
    path('new_media/', views.new_media_view, name='new_media'),
    path('new_album/', views.new_album_view, name='new_album'),
    path('<username>/', views.gallery_view, name='gallery'),

    path('<username>/<album_title>/', views.album_view, name='album'),  
    path('<username>/medias/<media_id>/', views.media_view, name='media'),
]
