from django.db import models

# Create your models here.
class News:
    def __init__(self, title, text, date):
        self.title = title
        self.text = text
        self.date = date

def __str__(self):
    return f'{self.title}: {self.text}, {self.date}'

class Product:
    counter = 0
    def __init__(self,title,price,quantity):
        self.title = title
        self.price = price
        self.quantity = quantity

        Product.counter +=1

    def amount(self):
        return self.price*self.quantity



# Для динамической таблицы
class Book(models.Model):
    name = models.CharField(max_length=100)