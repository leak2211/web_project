from django.shortcuts import render

def index(request):
    context = {
        'title': 'Главная страница',
        'welcome_text': 'Aboook - обменивайтесь книгами',
    }
    return render(request, 'Aboook/index.html', context)

def about(request):
    context = {
        'title': 'О нас',
    }
    return render(request, 'Aboook/about.html', context)