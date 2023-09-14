from rest_framework import serializers

from main.models import CourseSubscription, Payment, Well, Lesson
from main.validators import validate_youtube_link

class LessonSerializer(serializers.ModelSerializer):

   class Meta:
      model = Lesson 
      fields = '__all__'
      validators = [
         validate_youtube_link(fields='link_to_video')
      ]

class WellSerializer(serializers.ModelSerializer):
   lesson_count = serializers.SerializerMethodField()
   lessons = LessonSerializer(many=True, read_only=True)
   subscribed = serializers.SerializerMethodField()

   class Meta:
      model = Well 
      fields = '__all__'

   def get_lesson_count(self, obj):
      return obj.lessons.count()
   
   def get_subscribed(self, obj):
      user = self.context['request'].user
      try:
         subscription = CourseSubscription.objects.get(user=user, well=obj)
         return subscription.subscribed
      except CourseSubscription.DoesNotExist:
         return False
   
class PaymentSerializer(serializers.ModelSerializer):
   class Meta:
      model = Payment
      fields = '__all__' 

class CourseSubscriptionSerializer(serializers.ModelSerializer):
   class Meta:
      model = CourseSubscription
      fields = '__all__'