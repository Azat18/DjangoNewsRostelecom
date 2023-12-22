from django.contrib import admin
from .models import Demo

class DemoAdmin(admin.ModelAdmin):
    list_Display = ['title', 'image', 'image_tag']
# Register your models here.
admin.site.register(Demo,DemoAdmin)

