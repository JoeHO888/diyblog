from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blogs/', views.BlogListView.as_view(), name='blogs'),
    path('blog/<int:pk>', views.BlogDetailView.as_view(), name='blog-detail'),
    path('bloggers/', views.BloggerListView.as_view(), name='bloggers'),
    path('blogger/<int:pk>', views.BloggerDetailView.as_view(), name='blogger-detail'),
    # path('blog/<int:pk>/create/', views.CommentCreate.as_view(), name='make_comment'),
    path('blog/<int:pk>/create/', views.MakeComment, name='make_comment')
]