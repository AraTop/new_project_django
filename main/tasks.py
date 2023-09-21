from datetime import timedelta
import datetime
from celery import shared_task
from project import settings
from users.models import User
from django.core.mail import send_mail

@shared_task
def check_is_active():
   #inactive_period = timedelta(days=182)
   inactive_period = timedelta(minutes=5)
   cutoff_date = datetime.now() - inactive_period
   inactive_users = User.objects.filter(last_login=cutoff_date)
   
   for user in inactive_users:
      user.is_active = False
      user.save()

@shared_task
def send_update_email(user_email, course_name):
   subject = 'Обновление курса'
   message = f'Уважаемый пользователь, материалы курса "{course_name}" были обновлены.'
   from_email = settings.EMAIL_HOST_USER
   recipient_list = [user_email]
   print(user_email)

   send_mail(subject, message, from_email, recipient_list)