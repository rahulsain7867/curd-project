from django.contrib import admin

# Register your models here.
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "created_at", "updated_at")
    search_fields = ("title", "user__email")
    list_filter = ("created_at", "updated_at")