from django.db import models
from django.forms import forms
from django.utils.safestring import mark_safe

# Create your models here.
class Demo(models.Model):
    title = models.CharField(max_length=30)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))