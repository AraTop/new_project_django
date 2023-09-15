import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from .models import Well, Lesson, CourseSubscription
from rest_framework.test import APIClient

class LessonCRUDAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='user@user1.com',
            is_staff=True,
            is_superuser=True,
            is_active=True,)
        
        self.user.set_password('123')
        self.user.save()
        response = self.client.post('http://127.0.0.1:8000/users/token/', {"email": "user@user1.com", "password": "123"})
        response_data = json.loads(response.content)
        self.access_token = response_data.get('access')
        self.course = Well.objects.create(name='Test Course', description='Course Description')
        self.lesson = Lesson.objects.create(name='Test Lesson', description='Lesson Description', well=self.course)
        self.subscription = CourseSubscription.objects.create(user=self.user, well=self.course, subscribed=True)
        self.client = APIClient()

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
            'description': 'Updated Lesson Description',
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
        response = self.client.get(reverse('main:lesson_one', args=[self.course.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Подписан')

        response = self.client.post(reverse('main:create_subscription'), data={'well_id': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        updated_subscription = CourseSubscription.objects.get(user=self.user, well=self.course)
        self.assertTrue(updated_subscription.subscribed)

        response = self.client.delete(reverse('main:delete_subscription', args=[self.course.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        updated_subscription = CourseSubscription.objects.get(user=self.user, well=self.course)
        self.assertFalse(updated_subscription.subscribed)