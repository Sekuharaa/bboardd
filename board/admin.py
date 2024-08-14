from django.contrib import admin
from django import forms

from .models import Ad, User,Category,Comment
from ckeditor_uploader.widgets import CKEditorUploadingWidget


# Register your models here.
class AdAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Ad
        fields = '__all__'

class AdAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'created_at', 'update_at', 'user', 'category']
    form = AdAdminForm




admin.site.register(Ad, AdAdmin)
admin.site.register(User)
admin.site.register(Comment)