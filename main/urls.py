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
] + router.urls