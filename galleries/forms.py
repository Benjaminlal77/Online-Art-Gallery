from django import forms

from .models import *

class MediaUploadForm(forms.ModelForm, forms.ModelMultipleChoiceField):
    class Meta:
        model = MediaUpload
        exclude = ['published_date']

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = ['published_date']
        file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
