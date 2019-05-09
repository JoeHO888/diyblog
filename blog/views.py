from django.shortcuts import render

# Create your views here.

from blog.models import Blog, Author, Comment

def index(request):
    context = {
        'num_books': "s"
    }

    return render(request, 'index.html', context=context)
