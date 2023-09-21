import datetime
from rest_framework import viewsets, generics
import stripe
from main.models import CourseSubscription, Payment, Well, Lesson
from main.paginators import LessonPaginator, WellPaginator
from main.permissions import IsOwnerOrModerator, ModeratorPermission
from main.serialization import CourseSubscriptionSerializer, LessonSerializer, PaymentSerializer, WellSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import redirect, render
from main.tasks import send_update_email

from project import settings

class WellViewSet(viewsets.ModelViewSet):
   serializer_class = WellSerializer
   queryset = Well.objects.all()
   pagination_class = WellPaginator
   permission_classes = [IsAuthenticated]

   def perform_update(self, serializer):
      instance = serializer.save()

      user = self.request.user
      user_email = user.email
      
      course_name = instance.name
      send_update_email.delay(user_email, course_name)

class LessonCreateAPIView(generics.CreateAPIView):
   serializer_class = LessonSerializer
   permission_classes = [IsAuthenticated, IsOwnerOrModerator]

class LessonListAPIView(generics.ListAPIView):
   serializer_class = LessonSerializer
   queryset = Lesson.objects.all()
   pagination_class = LessonPaginator
   permission_classes = [IsAuthenticated, ModeratorPermission]

class LessonRetrieveAPIView(generics.RetrieveAPIView):
   serializer_class = LessonSerializer
   queryset = Lesson.objects.all()
   permission_classes = [IsAuthenticated, ModeratorPermission]

class LessonUpdateAPIView(generics.UpdateAPIView):
   serializer_class = LessonSerializer
   queryset = Lesson.objects.all()
   permission_classes = [IsAuthenticated, ModeratorPermission]

class LessonDestroyAPIView(generics.DestroyAPIView):
   queryset = Lesson.objects.all()
   permission_classes = [IsAuthenticated]

class PaymentListView(generics.ListCreateAPIView):
   queryset = Payment.objects.all()
   serializer_class = PaymentSerializer
   filter_backends = [DjangoFilterBackend, OrderingFilter]
   filterset_fields = ['user', 'course_or_lesson', 'id', 'payment_date', 'amount'] 
   permission_classes = [IsAuthenticated, ModeratorPermission]

class CourseSubscriptionView(APIView):
   permission_classes = [IsAuthenticated]

   def post(self, request):
      well_id = request.data.get('well_id')
      user = request.user

      try:
         subscription, created = CourseSubscription.objects.get_or_create(user=user, well_id=well_id)
         serializer = CourseSubscriptionSerializer(subscription)

         if created:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
         else:
            return Response(serializer.data, status=status.HTTP_200_OK)
      except Exception as e:
         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

   def delete(self, request, well_id):
      user = request.user

      try:
         subscription = CourseSubscription.objects.get(user=user, well_id=well_id)
         subscription.delete()
         return Response(status=status.HTTP_204_NO_CONTENT)
      except CourseSubscription.DoesNotExist:
         return Response({'error': 'Подписка не найдена'}, status=status.HTTP_404_NOT_FOUND)
      except Exception as e:
         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

def retrieve_payment(request, payment_intent_id):
   try:
      payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
      payment_info = {
         "id": payment_intent.id,
         "amount": payment_intent.amount,
         "currency": payment_intent.currency,
      }
      return render(request, 'main/retrieve_payment.html', {'payment_info': payment_info})
   except stripe.error.StripeError as e:
      print(f"Ошибка Stripe: {e}")
      return None
          
def create_payment(request, well_id):
   if request.method == 'POST':
      amount = 1000   #$10.00
      currency = 'usd'

      try:
         stripe.api_key = settings.STRIPE_SECRET_KEY
         payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency)

         payment_intent_id = payment_intent.id
         well = Well.objects.get(pk=well_id)
         payment = Payment(
            user=request.user,  
            payment_date=datetime.date.today(),
            course_or_lesson=well,
            amount=amount / 100,
            payment_method='Stripe'
         )
         payment.save()
         return redirect('main:ret', payment_intent_id=payment_intent_id)
         #return render(request, 'main/create_payment.html', {'client_secret': payment_intent.client_secret})
      
      except stripe.error.StripeError as e:
         print(f"Ошибка Stripe: {e}")

   return render(request, 'main/create_payment.html') 