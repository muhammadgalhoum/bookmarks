from django.contrib import admin, messages
from django.utils.text import slugify

from .models import Image

# Register your models here.


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'image', 'created']
    list_filter = ['created']
    search_fields = ['title', 'description']
    raw_id_fields = ['user']
    prepopulated_fields = {'slug': ('title',)}
    show_facets = admin.ShowFacets.ALWAYS
    
    def save_model(self, request, obj, form, change):
        # Check if the title is unique
        if Image.objects.filter(title=obj.title).exclude(pk=obj.pk).exists():
            self.message_user(request,
                              "This title already exists. Please choose a different title.", level=messages.ERROR)
        else:
            # Update the slug field based on the updated title
            obj.slug = slugify(obj.title)
            obj.save()
