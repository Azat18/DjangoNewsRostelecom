from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.db import connection, reset_queries
from django.views.generic import DetailView, DeleteView, UpdateView, ListView
from django.contrib.auth.decorators import login_required
from .forms import *
from django.urls import reverse_lazy
import json
from django.core.paginator import Paginator


#URL:    path('search_auto/', views.search_auto, name='search_auto'),
mimetype = 'application/json'
def search_auto(request):
    print('Запрос')
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':# Альтернатива if request.is_ajax()
        q = request.GET.get('term','')
        articles = Article.objects.filter(title__icontains=q)
        results =[]
        for a in articles:
            results.append(a.title)
            data = json.dumps(results)
    else:
        data = 'fail'
        # mimetype = 'application/json'
    return HttpResponse(data,mimetype)

class ArticleListView(ListView):
   model = Article
   template_name = 'article_list.html'
   context_object_name = "articles"


   def get_queryset(self):  # новый
       query = self.request.GET.get('search_input')
       articles = Article.objects.filter(title__icontains=query)
       return articles



def news(request):
   return render(request,'news/news.html')

from .utils import ViewCountMixin
class ArticleDetailView(ViewCountMixin, DetailView):
    model = Article
    template_name = 'news/news_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_object = self.object
        images = Image.objects.filter(article=current_object)
        context['images'] = images
        return context

class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'news/create_article.html'
    fields = ['title','anouncement','text','tags']

    def get_context_data(self, **kwargs):
        context = super(ArticleUpdateView, self).get_context_data(**kwargs)
        current_object = self.object
        images = Image.objects.filter(article=current_object)
        context['image_form'] = ImagesFormSet(instance=current_object)
        return context

    def post(self, request, **kwargs):
        current_object = Article.objects.get(id=request.POST['image_set-0-article'])
        deleted_ids = []
        for i in range(int(request.POST['image_set-TOTAL_FORMS'])):  # удаление всех по галочкам
            field_delete = f'image_set-{i}-DELETE'
            field_image_id = f'image_set-{i}-id'
            if field_delete in request.POST and request.POST[field_delete] == 'on':
                image = Image.objects.get(id=request.POST[field_image_id])
                image.delete()
                deleted_ids.append(field_image_id)
        # тут же удалить изображение из request.FILES
    # Замена изображения
        for i in range(int(request.POST['image_set-TOTAL_FORMS'])):  # удаление всех по галочкам
            field_replace = f'image_set-{i}-image'  # должен быть в request.FILES
            field_image_id = f'image_set-{i}-id'  # этот файл мы заменим
            if field_replace in request.FILES and request.POST[
                field_image_id] != '' and field_image_id not in deleted_ids:
                image = Image.objects.get(id=request.POST[field_image_id])  #
                image.delete()  # удаляем старый файл
                for img in request.FILES.getlist(field_replace):  # новый добавили
                    Image.objects.create(article=current_object, image=img, title=img.name)
                del request.FILES[field_replace]  # удаляем использованный файл
        if request.FILES:  # Добавление нового изображения
            print('!!!!!!!!!!!!!!!!!', request.FILES)
            for input_name in request.FILES:
                for img in request.FILES.getlist(input_name):
                    print('###############', img)
                    Image.objects.create(article=current_object, image=img, title=img.name)

        return super(ArticleUpdateView, self).post(request, **kwargs)


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('news_index') #именованная ссылка или абсолютную
    template_name = 'news/delete_article.html'

#человек не аутентифицирован - отправляем на страницу другую
# @login_required(login_url="/") Альтернатива ниже
from users.utils import check_group
from django.conf import settings
@login_required(login_url=settings.LOGIN_URL)
@check_group('Authors')
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            if current_user.id != None: #проверили что не аноним
                new_article = form.save(commit=False)
                new_article.author = current_user
                new_article.save() #сохраняем в БД
                form.save_m2m() #сохраняем теги
                # form = ArticleForm()
                for img in request.FILES.getlist('image_field'):
                    Image.objects.create(article=new_article, image=img, title=img.name)

                return redirect('news_index')
    else:
        form = ArticleForm()
    return render(request,'news/create_article.html', {'form':form})

from time import time

def index(request):
    # пример применения пользовательского менеджера
    # articles = Article.published.all()
    # it = Tag.objects.filter(title='IT').first()
    # print('IT использовалось: ',it.tag_count())

    categories = Article.categories  # создали перечень категорий
    author_list = User.objects.all()  # создали перечень авторов

    if request.method == "POST":
        selected_author = int(request.POST.get('author_filter'))
        selected_category = int(request.POST.get('category_filter'))

        if selected_author == 0:  # выбраны все авторы
            articles = Article.objects.all()
        else:
            articles = Article.objects.filter(author=selected_author)
        if selected_category != 0:  # фильтруем найденные по авторам результаты по категориям
            articles = articles.filter(category__icontains=categories[selected_category - 1][0])


    else:  # если страница открывется впервые
        selected_author = 0
        selected_category = 0
        articles = Article.objects.all()

    total = len(articles)

    p = Paginator(articles, 2)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    context = {'articles': page_obj, 'author_list': author_list, 'selected_author': selected_author,
               'categories': categories, 'selected_category': selected_category,'total':total,}
    return render(request, 'news/news_list.html', context)




def news_slider(request):
   categories = Article.categories  # создали перечень категорий
   author_list = User.objects.all()  # создали перечень авторов


   if request.method == "POST":
       selected_author = int(request.POST.get('author_filter'))
       selected_category = int(request.POST.get('category_filter'))


       if selected_author == 0:  # выбраны все авторы
           articles = Article.objects.all()
       else:
           articles = Article.objects.filter(author=selected_author)
       if selected_category != 0:  # фильтруем найденные по авторам результаты по категориям
           articles = articles.filter(category__icontains=categories[selected_category - 1][0])




   else:  # если страница открывется впервые
       selected_author = 0
       selected_category = 0
       articles = Article.objects.all()
   # сортировка от свежих к старым новостям
   articles = articles.order_by('-date')


   total = len(articles)


   p = Paginator(articles, 3)
   page_number = request.GET.get('page')
   page_obj = p.get_page(page_number)
   context = {'articles': page_obj, 'author_list': author_list, 'selected_author': selected_author,
              'categories': categories, 'selected_category': selected_category,'total':total,}


   return render(request, 'news/news_slider.html', context)

