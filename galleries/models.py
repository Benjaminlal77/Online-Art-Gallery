from django.db import models

class Album(models.Model):
    title = models.CharField(max_length=150)
    published_date = models.DateTimeField(auto_now_add=True)

class MediaUpload(models.Model):        
    albums = models.ManyToManyField(Album, blank=True)
    
    title = models.CharField(max_length=200,default='Untitled')
    artist = models.CharField(max_length=100,default='Unknown')
    file = models.FileField()
    published_date = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
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
