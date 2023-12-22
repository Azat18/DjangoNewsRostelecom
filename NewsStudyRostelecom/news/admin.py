from django.contrib import admin
from .models import *
from django.db.models.functions import Length
from django.db.models import Count

# Register your models here.
class ArticleFilter(admin.SimpleListFilter):
    title = 'По длине новости'
    parameter_name = 'text'

    def lookups(self, request, model_admin):
        return [('S',("Короткие, <100 зн.")),
                ('M',("Средние, 100-500 зн.")),
                ('L',("Длинные, >500 зн.")),]

    def queryset(self, request, queryset):
        if self.value() == 'S':
            return queryset.annotate(text_len=Length('text')).filter(text_len__lt=100)
        elif self.value() == 'M':
            return queryset.annotate(text_len=Length('text')).filter(text_len__lt=500,
                                                                    text_len__gte=100)
        elif self.value() == 'L':
            return queryset.annotate(text_len=Length('text')).filter(text_len__gt=500)
class ArticleImageInline(admin.TabularInline): # TabularInline вертикальный StackedInline горизонтальный
    model = Image #Какую модель нужно привязать к Article
    extra = 3 #Сколько полей мы хотели бы видеть на странице
    readonly_fields = ('id','image_tag') #Поля, которые не хотим менять
class ArticleAdmin(admin.ModelAdmin):
    ordering = ['-date', 'title', 'author']
    list_display = ['title', 'author', 'date', 'status', 'symbols_count', 'image_tag']
    list_filter = ['date', ArticleFilter]
    # list_display_links = ('date',)
    # list_editable = ['title']
    search_fields = ['title__icontains', 'tags__title'] # Можно применить look up функции __startswith, __icontains
    filter_horizontal = ['tags']
    prepopulated_fields = {"slug": ("title",)}
    list_per_page = 5
    inlines = [ArticleImageInline, ]
    #fields=['title', 'text']
    #exclude=['title', 'text']

    @admin.display(description='Длина', ordering='_symbols')
    def symbols_count(self, article: Article):
        return f"Символы: {len(article.text)}"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(_symbols=Length('text'))
        return queryset
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'tag_count']
    list_filter = ['title', 'status']
    actions = ['set_true', 'set_false']

    @admin.action(description='Деактивировать выбранные теги')
    def set_false(self, request, queryset):
        amount = queryset.update(status=False)
        self.message_user(request, f'Деактивировано {amount} тегов')

    @admin.action(description='Активировать выбранные теги')
    def set_true(self, request, queryset):
        amount = queryset.update(status=True)
        self.message_user(request, f'Активировано {amount} тегов')

    @admin.display(description='Использований', ordering='tag_count')
    def tag_count(self, object):
        return object.tag_count
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(tag_count=Count('article'))
        return queryset

admin.site.register(Article,ArticleAdmin)
# admin.site.register(Tag,TagAdmin)
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title','article','image_tag']

@admin.register(ViewCount)
class ViewCountAdmin(admin.ModelAdmin):
    list_display = ['article','ip_address','view_date']