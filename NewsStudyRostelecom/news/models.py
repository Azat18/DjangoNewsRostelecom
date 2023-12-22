from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.db.models import Count

class Tag(models.Model):
    title = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.title

    # def tag_count(self):
    #     count = self.article_set.count()
        # комментарий: когда мы работаем со связанными объектами (foreign_key, m2m, один к одному),
        # мы можем обращаться к связанным таблицам при помощи синтаксиса:
        # связаннаяМодель_set и что-то делать с результатами. В этом примере - мы используем связанные article
        # и вызываем метод count
        # return count
    class Meta:
        ordering = ['title', 'status']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

import datetime
class PublishedToday(models.Manager):
    def get_queryset(self):
        return super(PublishedToday,self).get_queryset().filter(date__gte=datetime.date.today())

class Article(models.Model):
   categories = (('C', 'Культура'),
                 ('B','Бизнес'),
                 ('S','Наука'),
                 ('N','Спорт'),
                 ('T', 'Путешествия'),
                 ('W', 'Погода'))
   #поля                           #models.CASCADE SET_DEFAULT
   author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
   title = models.CharField('Название', max_length=50,default='')
   anouncement = models.TextField('Аннотация', max_length=250)
   text = models.TextField('Текст новости')
   date = models.DateTimeField('Дата публикации', auto_now=True)
   category = models.CharField(choices=categories, max_length=25,verbose_name='Категории')
   tags = models.ManyToManyField(to=Tag, blank=True)
   status = models.BooleanField(default=False, verbose_name='Опубликовано')
   slug = models.SlugField()
   objects = models.Manager()
   published = PublishedToday()


   #методы моделей
   def __str__(self):
       return f'{self.title} от: {str(self.date)[:10]}'


   def get_absolute_url(self):
       return f'/news/show/{self.id}'


   # def tag_list(self):
   #     s = ''
   #     for t in self.tags.all():
   #         s+=t.title+' '
   #     return s


   def title_list(self):
       s = ''
       for t in self.title.all():
           s+=t.title+' '
           return s
   #метаданные модели
   def image_tag(self):
       image = Image.objects.filter(article=self)
       if image:
           return mark_safe(f'<img src="{image[0].image.url}" height="50px" width="auto" />')
       else:
           return '(no image)'


   def get_views(self):
       return self.views.count()
   class Meta:
       ordering = ['title','date']
       verbose_name= 'Новость'
       verbose_name_plural='Новости'

class Image(models.Model):
   article = models.ForeignKey(Article, on_delete=models.CASCADE)
   title = models.CharField(max_length=50, blank=True)
   image = models.ImageField(upload_to='article_images/', null=True, blank=True) #лучше добавить поле default !!!
   def __str__(self):
       return self.title
   def image_tag(self):
       if self.image is not None:
           return mark_safe(f'<img src="{self.image.url}" height="50px" width="auto" />')
       else:
           return '(no image)'

class ViewCount(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE,
                                related_name='views')
    ip_address = models.GenericIPAddressField()
    view_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('-view_date',)
        indexes = [models.Index(fields=['-view_date'])]

    def __str__(self):
        return self.article.title

