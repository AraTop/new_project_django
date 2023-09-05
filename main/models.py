from django.db import models

NULLABLE = {'null':True, 'blank':True}

class Well(models.Model):
   name = models.CharField(max_length=150 ,verbose_name='Название')
   preview = models.ImageField( verbose_name='Превью', **NULLABLE)
   description = models.TextField(verbose_name='Описание')

   def __str__(self):
      return f'{self.name} {self.description}' 
   
   class Meta:
      verbose_name = 'Курс'
      verbose_name_plural = 'Курсы'
      ordering = ('name',)

class Lesson(models.Model):
   name = models.CharField(max_length=150 ,verbose_name='Название')
   description = models.TextField(verbose_name='Описание')
   preview = models.ImageField( verbose_name='Превью', **NULLABLE)
   link_to_video = models.CharField(max_length=80, verbose_name='ссылка на видео', **NULLABLE)

   def __str__(self):
      return f'{self.name} {self.description}' 
   
   class Meta:
      verbose_name = 'Урок'
      verbose_name_plural = 'Уроки'
      ordering = ('name',)