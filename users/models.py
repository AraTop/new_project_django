from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {'null':True, 'blank':True}

class User(AbstractUser):
   username = None
   email = models.EmailField(unique=True, verbose_name='Почта')

   first_name = models.CharField(max_length=150, verbose_name='Имя')
   last_name = models.CharField(max_length=150, verbose_name='Фамилия')
   surname = models.CharField(max_length=200, verbose_name='Отчество', **NULLABLE)
   phone = models.CharField(max_length=50, verbose_name='Телефон', **NULLABLE)
   city = models.CharField(max_length=250, verbose_name='Город', **NULLABLE)
   avatar = models.ImageField(verbose_name='Аватарка', **NULLABLE)
   
   USERNAME_FIELD = "email"
   REQUIRED_FIELDS = []