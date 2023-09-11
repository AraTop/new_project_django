from rest_framework import viewsets, generics
from main.models import Payment, Well, Lesson
from main.permissions import IsOwnerOrModerator, ModeratorPermission
from main.serialization import LessonSerializer, PaymentSerializer, WellSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

class WellViewSet(viewsets.ModelViewSet):
   serializer_class = WellSerializer
   queryset = Well.objects.all()
   permission_classes = [IsAuthenticated]

class LessonCreateAPIView(generics.CreateAPIView):
   serializer_class = LessonSerializer
   permission_classes = [IsAuthenticated, IsOwnerOrModerator]

class LessonListAPIView(generics.ListAPIView):
   serializer_class = LessonSerializer
   queryset = Lesson.objects.all()
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
permission_classes = [IsAuthenticated, IsOwnerOrModerator]

class PaymentListView(generics.ListCreateAPIView):
   queryset = Payment.objects.all()
   serializer_class = PaymentSerializer
   filter_backends = [DjangoFilterBackend, OrderingFilter]
   filterset_fields = ['user', 'course_or_lesson', 'id', 'payment_date', 'amount'] 
   permission_classes = [IsAuthenticated, ModeratorPermission]