from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    year = models.IntegerField(verbose_name='Год издания')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    author = models.CharField(max_length=200, blank=True, verbose_name='Автор')

    def __str__(self):
        return f"{self.title} ({self.author})"

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['-created_at']