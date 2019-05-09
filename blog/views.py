from django.shortcuts import render

# Create your views here.

from blog.models import Blog, Blogger, Comment

def index(request):

    num_blog = Blog.objects.all().count()
    num_Blogger = Blogger.objects.all().count()
    num_comment = Comment.objects.all().count()

    context = {
        'num_blog': num_blog,
        'num_Blogger': num_Blogger,
        'num_comment': num_comment,

    }

    return render(request, 'index.html', context=context)
