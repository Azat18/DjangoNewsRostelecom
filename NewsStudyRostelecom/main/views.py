from django.shortcuts import render
from django.http import HttpResponse
from .models import News, Product, Book

def index(request):
    #value = 100
    # n1 = News('Новость 1', 'Текст 1', '05.05.2025')
    # n2 = News('Новость 2', 'Текст 2', '10.05.2025')
    # l = [n1, n2]
    # context = {'title': 'Страница главная',
    #            'header1': 'Заголовок страницы',
    #            }
    return render(request, 'magazine/homebase.html')

def get_demo(request,a,operation,b):
    if operation == 'minus':
        return HttpResponse(int(a) - int(b))
    elif operation == 'plus':
        return HttpResponse(int(a) + int(b))
    elif operation == 'multiply':
        return HttpResponse(int(a) * int(b))
    elif operation == 'divide':
        return HttpResponse(int(a) / int(b))
    elif operation == 'power':
        return HttpResponse(int(a) ** int(b))
    else:
        return HttpResponse('Нет данных')
def about(request):
    return render(request, 'main/about.html')

def content(request):
    return render(request, 'main/content.html')

def contacts(request):
    return render(request, 'main/contacts.html')

def sidebar(request):
    return render(request, 'main/sidebar.html')

def main(request):
    if request.method == 'POST':
        print('Получили POST-запрос')
        print(request.POST)
        title = request.POST.get('title')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        new_product = Product(title, float(price), int(quantity))
        print('Создан товар: ',new_product.title, 'Общая сумма: ', new_product.amount())
    else:
        print('Получили GET-запрос')
    # value = 100
    # n1 = News('Новость 1', 'Текст 1', '05.05.2025')
    # n2 = News('Новость 2', 'Текст 2', '10.05.2025')
    # l = [n1, n2]
    # d = {1:'Один', 'Сто':100}
    # context = {'title': 'Страница главная',
    #            'Header1': 'Заголовок страницы',
    #            # 'value': value,
    #            'numbers': l,
    #            'dictionary': d,}
    #
    # context['Пример'] = 'Example'
    water = Product('Минералка', 50, 10)
    chocolate = Product('Шоколадка', 100, 10)

    colors = ['black', 'blue', 'green', 'golden']
    context = {
        'colors': colors,
        'water': water,
        'chocolate': chocolate,
        }
    return render(request, 'main/main.html', context)

def menu(request):
    return render(request, 'main/menu.html')

# def page404(request, exeption, exception=None):
#     return render(request, 'magazine/page404.html')
#    #return HttpResponse(f'Ой: {exception}')

def account(request):
    return render(request, 'magazine/account.html')

# def news(request):
#     return render(request, 'news/news.html')

# def allnews(request):
#     return render(request, 'magazine/allnews.html')

def news_1(request):
    return render(request, 'magazine/news_1.html')
