from django.dispatch import receiver
from django.db.models.signals import post_save

from django.db import models
from django.contrib.auth.models import User

import magic

@receiver(post_save, sender=User)
def watchlist_create(sender, instance=None, created=False, **kwargs):
    if created:
        Album.objects.create(title='Recent', owner=instance)

class Album(models.Model):
    class Meta:
        unique_together = ['title', 'owner']
    title = models.CharField(max_length=150)
    published_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.deletion.CASCADE)
        
    def __init__(self, *args, **kwargs) -> None:
        def determine_preview_image_type():
            try:
                lastest_media_index = len(self.mediaupload_set.values('file')) - 1 
                lastest_media_url = self.mediaupload_set.values('file')[lastest_media_index]['file']
                self.preview_image = self.mediaupload_set.last()
                if self.preview_image.is_image:
                    self.preview_image_is_image = True
                    self.preview_image_is_video = False
                elif self.preview_image.is_video:
                    self.preview_image_is_image = False
                    self.preview_image_is_video = True
                    
                self.preview_image_url = '/medias/' + lastest_media_url
            except (IndexError, AssertionError, ValueError):
                pass

            
        super().__init__(*args, **kwargs)
        determine_preview_image_type()
        
    def __str__(self):
        return self.title

class MediaUpload(models.Model):            
    file = models.FileField()
    title = models.CharField(max_length=200, blank=True)
    artist = models.CharField(max_length=100, blank=True)
    tags = models.CharField(max_length=500, blank=True)

    albums = models.ManyToManyField(Album, blank=True)

    published_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.deletion.CASCADE)

    def __init__(self, *args, **kwargs) -> None:
        def determine_media_type():
            try:
                media_type = magic.from_file('static/medias/' + self.file.name, mime=True).split('/')[0]
                if media_type == 'image':
                    self.is_image = True
                    self.is_video = False
                elif media_type == 'video' or media_type == 'audio': # libmagic sometimes returns 'audio' for big video files
                    self.is_image = False
                    self.is_video = True
            except (FileNotFoundError, PermissionError):
                pass
                
        super().__init__(*args, **kwargs)
        
        determine_media_type()
    
    def tags_as_list(self):
        return self.tags.split('\n')
        
    def __str__(self):
        return self.title
            