from django.contrib import admin

from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'user', 'add_time', 'status', 'completion_date', )
    search_fields = ('id', 'title', 'user__username', )
    list_filter = ('add_time', 'status', )


admin.site.register(Task, TaskAdmin)
