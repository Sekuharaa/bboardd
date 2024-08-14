from string import hexdigits
from allauth.account.forms import SignupForm
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.core.mail import send_mail
from .models import Ad, Comment
import random
from django.conf import settings


class AdForm(forms.ModelForm):
    text = forms.CharField(label="Содержание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Ad
        fields = [
            'title',
            'text',
            'category',
        ]

class CommentForm(forms.ModelForm):
    text = forms.CharField(label='Текст комментария')

    class Meta:
        model = Comment
        fields = {
        'text'
        }

class CommonSignupForm(SignupForm):
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        user.is_active = False
        code = ''.join(random.sample(hexdigits, 5))
        user.code = code
        user.save()
        send_mail(
            subject='Код активации',
            message=f'Код активации аккаунта: {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return user