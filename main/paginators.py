from rest_framework.pagination import PageNumberPagination

class LessonPaginator(PageNumberPagination):
   page_size = 10 

class WellPaginator(PageNumberPagination):
   page_size = 10