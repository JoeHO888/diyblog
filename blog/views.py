from django.shortcuts import render
from django.views import generic
from blog.models import Blog, Blogger, Comment
from django.views.generic.list import MultipleObjectMixin
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



class BlogListView(generic.ListView):
    model = Blog
    paginate_by = 2

class BlogDetailView(generic.DetailView,MultipleObjectMixin):
    model = Blog
    paginate_by = 1

    def get_context_data(self, **kwargs):
        object_list = Comment.objects.filter(blog=self.object)
        context = super(BlogDetailView, self).get_context_data(object_list=object_list, **kwargs)
        return context


class BloggerListView(generic.ListView):
    model = Blogger

class BloggerDetailView(generic.DetailView,MultipleObjectMixin):
    model = Blogger
    paginate_by = 1

    def get_context_data(self, **kwargs):
        object_list = Blog.objects.filter(blogger=self.object)
        context = super(BloggerDetailView, self).get_context_data(object_list=object_list, **kwargs)
        return context

