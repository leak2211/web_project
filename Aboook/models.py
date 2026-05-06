from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название тега')
    slug = models.SlugField(max_length=50, unique=True, blank=True, verbose_name='Слаг')
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    year = models.IntegerField(verbose_name='Год издания')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    author = models.CharField(max_length=200, blank=True, verbose_name='Автор')
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='books',
        null=True,
        blank=True,
        verbose_name='Владелец'
    )
    
    image = models.ImageField(
        upload_to='books/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name='Изображение книги'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='books',
        verbose_name='Теги'
    )

    def __str__(self):
        return f"{self.title} ({self.author})"

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['-created_at']