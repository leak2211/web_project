from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import Book
from .forms import FeedbackForm   

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