from rest_framework import serializers

from main.models import Well, Lesson

class WellSerializer(serializers.ModelSerializer):
   
   class Meta:
      model = Well 
      fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):

   class Meta:
      model = Lesson 
      fields = '__all__'