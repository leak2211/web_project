from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'year', 'price', 'created_at')
    list_filter = ('year', 'created_at')
    search_fields = ('title', 'author')
    list_editable = ('price',)