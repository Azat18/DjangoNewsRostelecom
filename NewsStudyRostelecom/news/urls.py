from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('', views.news, name='news_index_1'),
   path('show/', views.index, name='news_index'),
   path('search_auto/', views.search_auto, name='search_auto'),
   path('article_list/', views.ArticleListView.as_view(), name='search_news'),
   path('show/<int:pk>', views.ArticleDetailView.as_view(), name='news_detail'),
   path('update/<int:pk>', views.ArticleUpdateView.as_view(), name='news_update'),
   path('delete/<int:pk>', views.ArticleDeleteView.as_view(), name='news_delete'),
   path('create', views.create_article, name='create_article'),
   # path('pagination',views.pagination,name='pagination'),
 ]

