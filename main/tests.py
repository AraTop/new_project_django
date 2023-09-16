import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from main.permissions import ModeratorPermission
from users.models import User
from .models import Well, Lesson, CourseSubscription
from rest_framework.test import APIClient
from django.contrib.auth.models import Group

class LessonCRUDAPITestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
        email='lololohka057@gmail.com',
        is_superuser=True,
        is_staff = True,
        is_active = True
        )
        self.user.set_password('12345')
        self.user.save()
        moderator, created = Group.objects.get_or_create(name='moderator')
        self.user.groups.add(moderator)
        response = self.client.post('http://127.0.0.1:8000/users/token/', {"email": "lololohka057@gmail.com", "password": "12345"})
        response_data = json.loads(response.content)
        self.access_token = response_data.get('access')
        self.course = Well.objects.create(name='Test Course', description='Course Description')
        self.lesson = Lesson.objects.create(name='Test Lesson', description='Lesson Description', well=self.course)
        self.subscription = CourseSubscription.objects.create(user=self.user, well=self.course, subscribed=True)

    def test_create_lesson(self):
        new_lesson_data = {
            'name': 'New Lesson',
            'description': 'New Lesson Description',
            'well': self.course.id,
            "link_to_video": "https://www.youtube.com/"
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post(reverse('main:lesson_create'), data=new_lesson_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_lesson(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(reverse('main:lesson_one', args=[self.lesson.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson(self):
        updated_lesson_data = {
            'name': 'Updated Lesson',
            'well': self.course.id,
            'description': 'Updated Lesson Description',
            "link_to_video": "https://www.youtube.com/"
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.put(reverse('main:lesson_update', args=[self.lesson.id]), data=updated_lesson_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.delete(reverse('main:lesson_delete', args=[self.lesson.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_course_subscription(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        response = self.client.post(reverse('main:create_subscription'), data={'well_id': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        course_subsc = CourseSubscription.objects.get(user=self.user, well=self.course)
        self.assertTrue(course_subsc.subscribed)
        
        response = self.client.delete(reverse('main:delete_subscription', args=[self.course.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        with self.assertRaises(CourseSubscription.DoesNotExist):
            CourseSubscription.objects.get(user=self.user, well=self.course)