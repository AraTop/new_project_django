from rest_framework import serializers

from main.models import Payment, Well, Lesson

class LessonSerializer(serializers.ModelSerializer):

   class Meta:
      model = Lesson 
      fields = '__all__'

class WellSerializer(serializers.ModelSerializer):
   lesson_count = serializers.SerializerMethodField()
   lessons = LessonSerializer(many=True, read_only=True)

   class Meta:
      model = Well 
      fields = '__all__'

   def get_lesson_count(self, obj):
      return obj.lessons.count()
   
class PaymentSerializer(serializers.ModelSerializer):
   class Meta:
      model = Payment
      fields = '__all__' 

