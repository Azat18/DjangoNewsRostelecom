"""
URL configuration for NewsStudyRostelecom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.magazine, name='magazine')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='magazine')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import handler404
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings
# import main.views as main_views
# handler404 = main_views.page404
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('magazine/', include('magazine.urls')),
    path('news/', include('news.urls')),
    path('users/', include('users.urls')),
    path('travel/', include('travel.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

   # ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug/__', include(debug_toolbar.urls)),
                  ] + urlpatterns

    urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
admin.site.site_header = "Панель администрирования новостей"
admin.site.index_title = "Новости нашего города"
admin.site.index_template = 'magazine/custom_admin.html'