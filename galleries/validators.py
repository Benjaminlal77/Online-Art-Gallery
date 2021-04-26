from django.core.exceptions import ValidationError

def validate_tags_format(tags):
    for tag in tags:
        print('Working tags')
        for character in tag:
            print('Getting Characters')
            if character == ' ':
                print('Validation Error')
                raise ValidationError('Do not put spaces in tags')    

def validate_media_file_extension(file):
    def is_image():
        valid_image_extensions = ['jpeg','jpg','png','gif','svg']
        return file_extension.lower() in valid_image_extensions
        
    def is_video():
        valid_video_extensions = ['mp4','mov','ogg','avi','m4v','mp2','mpg','mpv','webm']
        return file_extension.lower() in valid_video_extensions
    
    file_extension = file.name.split('.')[1]
    if not(is_image() or is_video()):
        raise ValidationError('Not valid media file extension')    
