from rest_framework import viewsets, generics
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

class WellViewSet(viewsets.ModelViewSet):
   serializer_class = WellSerializer
   queryset = Well.objects.all()
   pagination_class = WellPaginator
   permission_classes = [IsAuthenticated]

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