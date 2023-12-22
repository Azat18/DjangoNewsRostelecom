from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name = 'demo'),
    path('calc/<int:a>/<slug:operation>/<int:b>',views.get_demo),
    path('about/', views.about, name = 'about'),
    path('contacts/', views.contacts, name = 'contacts'),
    path('content/', views.content, name = 'content'),
    path('sidebar/', views.sidebar),
    path('main/', views.main),
    path('menu/', views.menu),
    path('account/', views.account),
    # path('allnews/', views.allnews),
    path('news_1/', views.news_1),
    # path('news/', views.news_1),
]


