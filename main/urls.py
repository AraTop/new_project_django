from django.urls import path
from main import views
from .apps import MainConfig
from rest_framework.routers import DefaultRouter

app_name = MainConfig.name

router = DefaultRouter()
router.register(r'wells',views.WellViewSet, basename='wells')

urlpatterns = [
   path('lesson/create/', views.LessonCreateAPIView.as_view(), name='lesson_create'),
   path('lesson/', views.LessonListAPIView.as_view(), name='lesson_list'),
   path('lesson/<int:pk>/', views.LessonRetrieveAPIView.as_view(), name='lesson_one'),
   path('lesson/update/<int:pk>/', views.LessonUpdateAPIView.as_view(), name='lesson_update'),
   path('lesson/delete/<int:pk>/', views.LessonDestroyAPIView.as_view(), name='lesson_delete'),
   path('payments/', views.PaymentListView.as_view(), name='payment-list'),
   path('create_subscription/', views.CourseSubscriptionView.as_view(), name='create_subscription'),
   path('delete_subscription/<int:well_id>/', views.CourseSubscriptionView.as_view(), name='delete_subscription'),

   path('create_payment/<int:well_id>', views.create_payment, name='create_payment'),
   path('retrieve_payment/<str:payment_intent_id>', views.retrieve_payment, name='ret'),
] + router.urls