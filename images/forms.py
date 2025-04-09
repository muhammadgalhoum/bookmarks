import requests
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django import forms

from .models import Image

        
class ImageCreateForm(forms.ModelForm):
    class Meta:
        model  = Image
        fields = ['title', 'url', 'description']
        widgets = {
            'url': forms.HiddenInput,
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title:
            if Image.objects.filter(title=title).exists():
                raise forms.ValidationError(
                    'This title already exists. Please choose a different title.'
                )
        return title
    
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png', 'webp', 'gif']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError(
                'The given URL does not match valid image extensions.'
            )
        return url
    
    def save(self, force_insert=False, force_update=False, commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'
        # download image from the given URL
        response = requests.get(image_url)
        image.image.save(
            image_name,
            ContentFile(response.content),
            save=False
        )
        if commit:
            image.save()
        return image


class ImageUpdateForm(forms.ModelForm):
    class Meta:
        model  = Image
        fields = ['title', 'url', 'image', 'description']
