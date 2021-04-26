from django.db import models
from django.contrib.auth.models import User
from .validators import *

class Album(models.Model):
    title = models.CharField(max_length=150)
    published_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.deletion.CASCADE)

    def __str__(self):
        return self.title

class MediaUpload(models.Model):            
    file = models.FileField(validators=[validate_media_file_extension])
    title = models.CharField(max_length=200, blank=True)
    artist = models.CharField(max_length=100, blank=True)
    tags = models.CharField(max_length=500, validators=[validate_tags_format], blank=True)

    albums = models.ManyToManyField(Album, blank=True)

    published_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.deletion.CASCADE)

    def __init__(self, *args, **kwargs) -> None:
        def find_file_type():                
            def check_if_is_image():
                valid_image_extensions = ['jpeg','jpg','png','gif','svg']
                return file_extension.lower() in valid_image_extensions          
            def check_if_is_video():
                valid_video_extensions = ['mp4','mov','ogg','avi','m4v','mp2','mpg','mpv','webm']
                return file_extension.lower() in valid_video_extensions

            try:
                file_extension = self.file.name.split('.')[1]
                self.is_image = check_if_is_image()
                self.is_video = check_if_is_video()
            except IndexError:
                pass

        def check_char_fields():
            def is_empty(char_field):
                return char_field == ''
        
            if is_empty(self.title):
                self.title = 'Untitled'
            if is_empty(self.artist):
                self.artist = 'Unknown'
            
        def check_tags():    
            self.tags = [tag for tag in self.tags.split(',')]
            
        super().__init__(*args, **kwargs)
        
        check_char_fields()
        check_tags()
        find_file_type()
        
    def __str__(self):
        return self.title
            