from django.shortcuts import render
from django.views import generic
from blog.models import Blog, Blogger, Comment
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.edit import CreateView
import datetime 
from django.urls import reverse,reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.forms import CommentForm
from django.http import HttpResponseRedirect,HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

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

class CommentCreate(LoginRequiredMixin,CreateView):
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        blog = Blog.objects.get(id=self.kwargs['pk'])
        form.instance.blog = blog
        form.instance.datetime = datetime.datetime.now() 
        form.instance.commenter = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog-detail', kwargs={'pk': self.kwargs['pk']})

class BlogListView(generic.ListView):
    model = Blog
    paginate_by = 2

class BlogDetailView(generic.DetailView,MultipleObjectMixin):
    model = Blog
    paginate_by = 1

    def get_context_data(self, **kwargs):
        object_list = Comment.objects.filter(blog=self.object)
        context = super(BlogDetailView, self).get_context_data(object_list=object_list, **kwargs)
        context['form'] = CommentForm()
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

@login_required
def MakeComment(request, pk):
    blog = Blog.objects.get(id=pk)
    form = CommentForm(request.POST)
    form.instance.blog = blog
    form.instance.datetime = timezone.now() 
    form.instance.commenter = request.user

    if form.is_valid():
        form.save()
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

def RegistrationConfirmationEmail(request):
    return render(request,'auth/user_form_done.html')

class UserRegister(CreateView):
    model = User
    fields = ['username','email','password']
    success_url = reverse_lazy('register-done')

    def form_valid(self, form):
        form.instance.is_active = False
        response = super(UserRegister, self).form_valid(form)
        return response



