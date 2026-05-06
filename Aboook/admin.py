from django.contrib import admin
from .models import Book, Tag

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'year', 'price', 'created_at')
    list_filter = ('year', 'created_at', 'tags')
    search_fields = ('title', 'author')
    list_editable = ('price',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}