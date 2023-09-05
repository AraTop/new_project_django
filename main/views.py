from django.shortcuts import render
from rest_framework import viewsets, generics
from main.models import Well, Lesson
from main.serialization import LessonSerializer, WellSerializer

class WellViewSet(viewsets.ModelViewSet):
   serializer_class = WellSerializer
   queryset = Well.objects.all()

class LessonCreateAPIView(generics.CreateAPIView):
   serializer_class = LessonSerializer

class LessonListAPIView(generics.ListAPIView):
   serializer_class = LessonSerializer
   queryset = Lesson.objects.all()

class LessonRetrieveAPIView(generics.RetrieveAPIView):
   serializer_class = LessonSerializer
   queryset = Lesson.objects.all()

class LessonUpdateAPIView(generics.UpdateAPIView):
   serializer_class = LessonSerializer
   queryset = Lesson.objects.all()

class LessonDestroyAPIView(generics.DestroyAPIView):
   queryset = Lesson.objects.all()