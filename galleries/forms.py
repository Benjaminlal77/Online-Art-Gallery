from django import forms

from .models import *

class MediaUploadForm(forms.ModelForm, forms.ModelMultipleChoiceField):
    class Meta:
        model = MediaUpload
        exclude = ['published_date', 'owner']
        widgets = {'file':forms.FileInput(attrs={'class':'custom-file-input', 'id':'file-input', 'accept':'image/*,video/*','multiple':'true'}),
                   'title':forms.TextInput(attrs={'class':'form-control', 'id':'title', 'placeholder':'Enter title'}),
                   'artist':forms.TextInput(attrs={'class':'form-control', 'id':'artist', 'placeholder':'Enter artist'}),
                   'tags':forms.TextInput(attrs={'class':'form-control', 'id':'tags', 'placeholder':'Enter tags'}),
                   'albums':forms.SelectMultiple(attrs={'class':'form-control', 'id':'albums'})}
    
    def __init__(self, user, *args, **kwargs):
        super(MediaUploadForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['albums'].queryset = Album.objects.filter(owner=user).order_by('-published_date')

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = ['published_date', 'owner']
        widgets = {'title':forms.TextInput(attrs={'class':'form-control', 'id':'title', 'placeholder':'Enter title'})}
