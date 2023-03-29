from tkinter.filedialog import SaveAs
from django.contrib import admin
from django import forms
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.safestring import mark_safe
from mptt.admin import MPTTModelAdmin

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

class PostEdited(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'

class PostAdmin(admin.ModelAdmin):
    form = PostEdited
    prepopulated_fields = {'slug': ('title',)}
    save_as = True
    readonly_fields = ['views', 'get_photo']
    list_display = ('title', 'get_photo')

    def get_photo(request, object):
        return mark_safe(f'<img src={object.photo.url} width=80>')
    
    
    get_photo.short_description = 'jjk'

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

class CommentAdmin(MPTTModelAdmin):
    pass #for subsequent registration

    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

