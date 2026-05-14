from django import forms
from .models import Book, Tag, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class FeedbackForm(forms.Form):
    subject = forms.CharField(
        max_length=200,
        label='Тема',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Например: Вопрос о книге'
        })
    )
    
    email = forms.EmailField(
        label='Ваш Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@mail.ru'
        })
    )
    
    text = forms.CharField(
        label='Сообщение',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Напишите ваше сообщение здесь...'
        })
    )


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'year', 'price', 'image', 'tags']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название книги'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите автора'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Введите описание книги'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Год издания'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Цена (0 - для бесплатного обмена)',
                'step': '0.01'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'size': 5
            }),
        }
        
        labels = {
            'title': 'Название книги',
            'author': 'Автор',
            'description': 'Описание',
            'year': 'Год издания',
            'price': 'Цена',
            'image': 'Изображение книги',
            'tags': 'Теги (можно выбрать несколько)',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Напишите ваш комментарий...'
            }),
        }
        labels = {
            'text': '',
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'
            self.fields[field_name].widget.attrs['placeholder'] = self.fields[field_name].label