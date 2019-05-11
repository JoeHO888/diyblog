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
from django.core.mail import send_mail
from django.conf import settings

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
    fields = ['username','email','password','first_name','last_name']
    success_url = reverse_lazy('register-done')

    def form_valid(self, form):
        form.instance.is_active = False
        response = super(UserRegister, self).form_valid(form)
        activation_message, activation_message_html = self.create_activation_message(form)
        send_mail(
            'Registration Confirmation',
            activation_message,
            settings.EMAIL_HOST_USER,
            [form.instance.email],
            fail_silently=False,
            html_message = activation_message_html
        )
        return response
    
    def create_activation_message(self,form):
        link = self.request.META['HTTP_HOST']+"/accounts/activation/abcd"+str(form.instance.id)
        activation_message = f''' 
        Hi {form.instance.first_name} {form.instance.last_name},
                                  
        Please Click the linke here to activate your account.
        http://{link}{link}
                                          
        Regards,
        Blog Team.
        '''

        activation_message_html = f''' 
        <p>Hi {form.instance.first_name} {form.instance.last_name},</p>
                                  
        <p>Please Click the linke here to activate your account.</p>
        <a href=http://{link}>http://{link}</a>
                                          
        <p>Regards,</p>
        <p>Blog Team.</p>
        '''
        return activation_message, activation_message_html


def ActivateAccount(request,token):
    id = int(token[4:])
    print(id)
    user = User.objects.get(id=id)
    if not user.is_active:
        user.is_active = True
        user.save()
    return HttpResponseRedirect(reverse('index'))
