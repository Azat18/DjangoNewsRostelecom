from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    gender_choices=(('M', 'Male'),
                    ('F', 'Female'),
                    ('N/A', 'No answers'))
    user = models.OneToOneField(User,on_delete=models.CASCADE,
                                primary_key=True)
    nickname = models.CharField(max_length=100)
    birthday = models.DateField(null=True)
    gender = models.CharField(choices=gender_choices,max_length=25,null=True)
    account_image = models.ImageField(default='default.jpg',
                                      upload_to='account_images')
    address = models.CharField(max_length=100,null=True)
    vk = models.CharField(max_length=100,null=True)
    telegram = models.CharField(max_length=100,null=True)
    phone = models.CharField(max_length=20,null=True)

    def __str__(self):
        return f"{self.nickname}'s account"

    class Meta:
        ordering = ['user']
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

from news.models import Article
class FavoriteArticle(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    article = models.ForeignKey(Article,on_delete=models.SET_NULL,null=True)
    create_at=models.DateTimeField(auto_now_add=True)
