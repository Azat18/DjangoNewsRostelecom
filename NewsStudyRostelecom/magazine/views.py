from django.shortcuts import render
from django.http import HttpResponse
from .forms import DemoForm, Demo
from news.models import Article
def index(request):
    #Примеры values
    # all_news = Article.objects.all().values('author','title')
    # # for a in all_news:
    # #     print(a['author'], a['title'])
    # all_news = Article.objects.all().values_list('title')
    # print(all_news)
    # all_news = Article.objects.all().values_list('title', flat=True)
    # print(all_news)
    # По старому
    # article = Article.objects.get(id=1)
    # print(article.author.username)
    # По новому
    # article = Article.objects.select_related('author').get(id=1)
    # print(article.author.username)

    # Многие ко многим не используя Prefetch_related
    # articles = Article.objects.all()
    # for a in articles:
    #     print(a.title, a.tags.all())
    # Многие ко многим с Prefetch_related
    # articles = Article.objects.prefetch_related('tags').all()
    # for a in articles:
    #     print(a.title, a.tags.all())
    # Пример аннтоирования и агрегации
    from django.db.models import Count, Avg, Max
    from django.contrib.auth.models import User

    # count_articles = User.objects.annotate(Count('article', distinct=True))
    # for user in count_articles:
    #     print(user, user.article__count)
    # Пример аннтоирования и агрегации для исключения дублей при 1 ко многим
    # count_articles = User.objects.annotate(Count('article', distinct=True)).aggregate(Avg('article__count'))
    # print(count_articles)
    # пример аннотирования и агрегации:
    # max_article_count_user = User.objects.annotate(Count('article', distinct=True)).order_by('-article__count').first()
    # print(max_article_count_user)

    max_article_count = User.objects.annotate(Count('article', distinct=True)).aggregate(Max('article__count'))
    max_article_count_user2 = User.objects.annotate(Count('article', distinct=True)).filter(
        article__count__exact=max_article_count['article__count__max'])
    print(max_article_count_user2)

    #return render(request, 'general.html')
    return render(request, 'magazine/index.html')
def account(request):

    return render(request, 'account/contact_page.html')

# def allnews(request):
#     return render(request, 'allnews/contact_page.html')
def news(request):
    return render(request,'magazine/news.html')

def news_1(request):
    return render(request, 'news_1/contact_page.html')

def demoform(request):
    form = DemoForm()
    if request.method == 'POST':
        new_model = DemoForm(request.POST,request.FILES)
        new_model.save()
    context = {'form':form}
    return render(request, 'magazine/image_Form.html', context)


def showlastmodel(request):
    model = Demo.objects.all().first()
    context = {'model': model}
    return render(request, 'magazine/image_Form.html', context)
# def page404(request):
#     return render(request, 'page404.html')