from django.contrib import admin

from .models import Todo


class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'completed', 'created_at', 'updated_at')
    list_filter = ('id',)


admin.site.register(Todo, TodoAdmin)
