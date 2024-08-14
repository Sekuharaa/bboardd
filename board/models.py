from django.contrib.auth.models import AbstractUser
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse


# Create your models here.
class User(AbstractUser):
    code = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Ad(models.Model):

    CATEGORY_CHOICES = [
        ('TANK', 'Танки'),
        ('HEALER', 'Хилы'),
        ('DPS', 'ДД'),
        ('MERCHANT', 'Торговцы'),
        ('GUILDMASTER', 'Гилдмастеры'),
        ('QUESTGIVER', 'Квестгиверы'),
        ('BLACKSMITH', 'Кузнецы'),
        ('LEATHERWORKER', 'Кожевники'),
        ('POTION_MASTER', 'Зельевары'),
        ('SPELLMASTER', 'Мастера заклинаний'),
    ]

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    text = RichTextUploadingField(verbose_name="Содержание")
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ad_detail', args=[str(self.id)])

class Comment(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, verbose_name='Объявление')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    status = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('ad_detail', args=[str(self.ad.id)])


