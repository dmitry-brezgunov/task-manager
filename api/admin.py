from django.contrib import admin

from .models import Task, TaskHistory


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'user', 'add_date', 'status', 'completion_date', )

    search_fields = ('id', 'title', 'user__username', )
    list_filter = ('add_date', 'status', )


class TaskHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'user', 'task', 'edit_time', )

    search_fields = ('id', 'title', 'user__username', 'task__id', )
    list_filter = ('add_date', 'status', 'edit_time', )


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskHistory, TaskHistoryAdmin)
