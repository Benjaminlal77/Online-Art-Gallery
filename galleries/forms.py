from django import forms
from django.core.exceptions import ValidationError

from .models import *

class MediaUploadForm(forms.ModelForm, forms.ModelMultipleChoiceField):
    class Meta:
        model = MediaUpload
        exclude = ['published_date', 'owner']
        widgets = {'file':forms.FileInput(attrs={'class':'custom-file-input', 'id':'file-input', 'accept':'image/*,video/*','multiple':'true', 'required':'true'}),
                   'title':forms.TextInput(attrs={'class':'form-control', 'id':'title-input', 'placeholder':'Enter title'}),
                   'artist':forms.TextInput(attrs={'class':'form-control', 'id':'artist-input', 'placeholder':'Enter artist'}),
                   'tags':forms.TextInput(attrs={'class':'form-control spaceless-input', 'id':'tags-input', 'placeholder':'Enter tags'}),
                   'albums':forms.SelectMultiple(attrs={'class':'form-control', 'id':'albums-input'})}
    
    def __init__(self, user, *args, **kwargs):
        super(MediaUploadForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['albums'].queryset = Album.objects.filter(owner=user).exclude(title='Recent').order_by('-published_date')

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = ['published_date', 'owner']
        widgets = {'title':forms.TextInput(attrs={'class':'form-control spaceless-input', 'id':'title-input', 'placeholder':'Enter title', 'required':'true'})}
    
    def __init__(self, user, *args, **kwargs):
        super(AlbumForm, self).__init__(*args, **kwargs)
        self.user = user
    
    def clean(self):
        try:
            Album.objects.get(title=self.cleaned_data['title'], owner=self.user)
        except Album.DoesNotExist:
            pass
        else:
            raise ValidationError('You already have an album named "' + self.cleaned_data['title'] + '"!')

        return self.cleaned_data
