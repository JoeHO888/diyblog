from django.contrib import admin

# Register your models here.

from blog.models import Blogger, Blog, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra  = 0

class BlogInline(admin.TabularInline):
    model = Blog
    extra  = 0

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title',  'date','display_most_recent_comment')
    # list_filter = ( 'date')
    inlines = [CommentInline]

@admin.register(Blogger)
class BloggerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth','date_of_death')
    inlines = [BlogInline]
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('commentId', 'blog', 'commenter','date')
    list_filter = ('blog', 'commenter')