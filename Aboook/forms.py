from django import forms
from .models import Book   

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
        fields = ['title', 'author', 'description', 'year', 'price']
        
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
        }
        
        labels = {
            'title': 'Название книги',
            'author': 'Автор',
            'description': 'Описание',
            'year': 'Год издания',
            'price': 'Цена',
        }