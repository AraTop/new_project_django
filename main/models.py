from django.db import models
from users.models import User

PAYMENT_METHOD_CHOICES = (
   ('cash', 'Наличные'),  
   ('transfer', 'Перевод на счет'),
)

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
   well = models.ForeignKey(Well, on_delete=models.CASCADE, related_name='lessons')

   def __str__(self):
      return f'{self.name} {self.description}' 
   
   class Meta:
      verbose_name = 'Урок'
      verbose_name_plural = 'Уроки'
      ordering = ('name',)
   
class Payment(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
   payment_date = models.DateField(verbose_name='Дата оплаты')
   course_or_lesson = models.ForeignKey(Well, on_delete=models.CASCADE, verbose_name='Оплаченный курс или урок')
   amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
   payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, verbose_name='Способ оплаты')

   def __str__(self):
      return f'{self.user} - {self.payment_date}'
   
   class Meta:
      verbose_name = 'Платеж'
      verbose_name_plural = 'Платежы'
      ordering = ('user',)

class CourseSubscription(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   well = models.ForeignKey(Well, on_delete=models.CASCADE)
   subscribed = models.BooleanField(default=True)

   def __str__(self):
      return f'{self.user} - {self.well}'
   
   class Meta:
      unique_together = ('user', 'well')
      verbose_name = 'Падписка'
      verbose_name_plural = 'Падписки'
      ordering = ('user',)