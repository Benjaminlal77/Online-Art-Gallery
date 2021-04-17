from django import forms

from .models import *

class MediaUploadForm(forms.ModelForm, forms.ModelMultipleChoiceField):
    class Meta:
        model = MediaUpload
        exclude = ['published_date', 'owner']
                
    def __init__(self, user, *args, **kwargs):
        super(MediaUploadForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['albums'].queryset = Album.objects.filter(owner=user).order_by('-published_date')

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = ['published_date', 'owner']
