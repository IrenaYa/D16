from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from ckeditor_uploader.fields import RichTextUploadingField

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('tank', 'Танки'),
        ('heal', 'Хилы'),
        ('DD', 'ДД'),
        ('traders', 'Торговцы'),
        ('gildemasters', 'Гилдмастеры'),
        ('quest', 'Квестгиверы'),
        ('blacksmiths', 'Кузнецы'),
        ('tanners', 'Кожевники'),
        ('potion', 'Зельевары'),
        ('spellmasters', 'Мастера заклинаний'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=12, choices=CATEGORY_CHOICES, default='tank')
    dateCreation = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, default='Заголовок')
    text = models.TextField()

    def __str__(self):
        return f'{self.id} : {self.title} : {self.text}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

class UserResponse(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    response_time = models.DateTimeField(auto_now_add=True)
    text = models.TextField(default='Текст отклика')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.author}: {self.text[:10]}'