from django.contrib import admin

from main.models import Well , Lesson

@admin.register(Well)
class SettingsAdmin(admin.ModelAdmin):
   list_display = ('name', 'preview', 'description')

@admin.register(Lesson)
class SettingsAdmin(admin.ModelAdmin):
   list_display = ('name', 'description', 'preview', 'link_to_video')