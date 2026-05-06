from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Book
from .forms import FeedbackForm, BookForm


def index(request):
    books = Book.objects.all()
    context = {
        'title': 'Главная страница',
        'welcome_text': 'Aboook - обменивайтесь книгами',
        'books': books,
    }
    return render(request, 'Aboook/index.html', context)

def about(request):
    context = {
        'title': 'О нас',
    }
    return render(request, 'Aboook/about.html', context)

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    context = {
        'title': book.title,
        'book': book,
    }
    return render(request, 'Aboook/detail.html', context)

def contact(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            print('=' * 50)
            print('НОВОЕ СООБЩЕНИЕ ОТ ПОЛЬЗОВАТЕЛЯ:')
            print(f'Тема: {form.cleaned_data["subject"]}')
            print(f'Email: {form.cleaned_data["email"]}')
            print(f'Сообщение: {form.cleaned_data["text"]}')
            print('=' * 50)
            return redirect('home')
    else:
        form = FeedbackForm()
    
    context = {
        'title': 'Контакты',
        'form': form,
    }
    return render(request, 'Aboook/contact.html', context)


@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False) 
            book.owner = request.user       
            book.save()                    
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()
    
    context = {
        'title': 'Добавление книги',
        'form': form,
        'button_text': 'Добавить книгу',
    }
    return render(request, 'Aboook/book_form.html', context)

@login_required
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if book.owner != request.user:
        return redirect('book_detail', pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    
    context = {
        'title': 'Редактирование книги',
        'form': form,
        'button_text': 'Сохранить изменения',
        'book': book,
    }
    return render(request, 'Aboook/book_form.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    
    context = {
        'title': 'Регистрация',
        'form': form,
    }
    return render(request, 'registration/register.html', context)