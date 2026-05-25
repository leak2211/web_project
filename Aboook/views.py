from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth import login as auth_login
from .models import Book, Tag, Comment
from .forms import BookForm, CommentForm, CustomUserCreationForm, FeedbackForm


class BookListView(ListView):
    model = Book
    template_name = 'Aboook/index.html'
    context_object_name = 'books'
    ordering = ['-created_at']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['welcome_text'] = 'Aboook - обменивайтесь книгами'
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'Aboook/detail.html'
    context_object_name = 'book'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['comments'] = self.object.comments.all()
        context['comment_form'] = CommentForm()
        return context


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'Aboook/book_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление книги'
        context['button_text'] = 'Добавить книгу'
        return context
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, f'Книга "{form.instance.title}" успешно добавлена!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk': self.object.pk})


class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'Aboook/book_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование книги'
        context['button_text'] = 'Сохранить изменения'
        return context
    
    def test_func(self):
        book = self.get_object()
        return self.request.user == book.owner
    
    def form_valid(self, form):
        messages.success(self.request, f'Книга "{form.instance.title}" успешно обновлена!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk': self.object.pk})


class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    template_name = 'Aboook/book_confirm_delete.html'
    success_url = reverse_lazy('home')
    
    def test_func(self):
        book = self.get_object()
        return self.request.user == book.owner
    
    def delete(self, request, *args, **kwargs):
        book = self.get_object()
        messages.success(request, f'Книга "{book.title}" успешно удалена!')
        return super().delete(request, *args, **kwargs)


class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    http_method_names = ['post']
    
    def form_valid(self, form):
        book = get_object_or_404(Book, pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        form.instance.book = book
        messages.success(self.request, 'Ваш комментарий успешно добавлен!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk': self.kwargs['pk']})


class ContactView(FormView):
    template_name = 'Aboook/contact.html'
    form_class = FeedbackForm
    success_url = reverse_lazy('contact')
    
    def form_valid(self, form):
        print('=' * 50)
        print('НОВОЕ СООБЩЕНИЕ ОТ ПОЛЬЗОВАТЕЛЯ:')
        print(f'Тема: {form.cleaned_data["subject"]}')
        print(f'Email: {form.cleaned_data["email"]}')
        print(f'Сообщение: {form.cleaned_data["text"]}')
        print('=' * 50)
        messages.success(self.request, 'Ваше сообщение успешно отправлено! Мы ответим вам в ближайшее время.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при отправке сообщения. Проверьте заполнение полей.')
        return super().form_invalid(form)


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        user = form.save()
        auth_login(self.request, user)
        messages.success(self.request, f'Добро пожаловать, {user.username}! Регистрация прошла успешно.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при регистрации. Проверьте введенные данные.')
        return super().form_invalid(form)


class BooksByTagView(ListView):
    model = Book
    template_name = 'Aboook/index.html'
    context_object_name = 'books'
    
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs['tag_id'])
        return tag.books.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(Tag, pk=self.kwargs['tag_id'])
        context['title'] = f'Книги с тегом: {tag.name}'
        context['welcome_text'] = f'Книги с тегом "{tag.name}"'
        return context