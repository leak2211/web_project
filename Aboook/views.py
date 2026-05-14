from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book, Tag, Comment
from .forms import FeedbackForm, BookForm, CommentForm, CustomUserCreationForm


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
    comments = book.comments.all()  
    comment_form = CommentForm()
    
    context = {
        'title': book.title,
        'book': book,
        'comments': comments,
        'comment_form': comment_form,
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
            messages.success(request, 'Ваше сообщение успешно отправлено! Мы ответим вам в ближайшее время.')
            return redirect('contact')
        else:
            messages.error(request, 'Ошибка при отправке сообщения. Проверьте заполнение полей.')
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
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.user
            book.save()
            form.save_m2m()
            messages.success(request, f'Книга "{book.title}" успешно добавлена!')
            return redirect('book_detail', pk=book.pk)
        else:
            messages.error(request, 'Ошибка при добавлении книги. Проверьте заполнение полей.')
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
        messages.error(request, 'Вы не можете редактировать эту книгу.')
        return redirect('book_detail', pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Книга "{book.title}" успешно обновлена!')
            return redirect('book_detail', pk=book.pk)
        else:
            messages.error(request, 'Ошибка при обновлении книги. Проверьте заполнение полей.')
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
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}! Регистрация прошла успешно.')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка при регистрации. Проверьте введенные данные.')
    else:
        form = CustomUserCreationForm()
        for field_name in form.fields:
            form.fields[field_name].widget.attrs['class'] = 'form-control'
    
    context = {
        'title': 'Регистрация',
        'form': form,
    }
    return render(request, 'registration/register.html', context)

def books_by_tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    books = tag.books.all()
    context = {
        'title': f'Книги с тегом: {tag.name}',
        'books': books,
        'current_tag': tag,
    }
    return render(request, 'Aboook/index.html', context)

@login_required
def add_comment(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.book = book
            comment.save()
            messages.success(request, 'Ваш комментарий успешно добавлен!')
        else:
            messages.error(request, 'Ошибка при добавлении комментария. Пожалуйста, попробуйте снова.')
    
    return redirect('book_detail', pk=book.pk)