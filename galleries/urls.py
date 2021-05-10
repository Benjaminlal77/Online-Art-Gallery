from django.urls import path

from . import views

urlpatterns = [
    path('', views.galleries_view, name='galleries'),
    path('new_media/', views.new_media_view, name='new_media'),
    path('new_album/', views.new_album_view, name='new_album'),
    path('<username>/medias/<media_id>/', views.media_view, name='media'),
    path('<username>/medias/<media_id>/delete_media/', views.delete_media, name='delete_media'),
    path('<username>/<int:page_num>/', views.gallery_view, name='gallery'),

    path('<username>/<album_title>/<int:page_num>/', views.album_view, name='album'),
    path('<username>/<album_title>/delete_album/', views.delete_album, name='delete_album'),
]
