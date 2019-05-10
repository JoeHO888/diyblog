from django.db import models

from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User
import uuid

class Comment(models.Model):
    commentId = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique Comment ID')
    content = models.CharField(max_length=200000)
    blog = models.ForeignKey('Blog', on_delete=models.SET_NULL, null=True)
    commenter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(null=False)

    class Meta: 
        ordering = ['date']

    def display_truncated_content(self):
        if len(self.content)>=72:
            return self.content[:71]+"..."
        else:
            return self.content
    
    display_truncated_content.short_description = 'Truncated Content (75 Characters)'

    def __str__(self):
        return self.content


class Blog(models.Model):
    title = models.CharField(max_length=200)
    blogger = models.ForeignKey('Blogger', on_delete=models.SET_NULL, null=True)
    post = models.TextField(max_length=10000000, help_text='Enter a blog post')
    date = models.DateField(null=False)

    class Meta: 
        ordering = ['-date']
    
    def display_truncated_post(self):
        if len(self.post)>=72:
            return self.post[:71]+"..."
        else:
            return self.post

    def display_most_recent_comment(self):
        comment = "No " or Comment.objects.filter(blog=self.id)[0].content
        return comment
    
    display_most_recent_comment.short_description = 'Most Recent Comment'
    
    def __str__(self):
        """String for representing the Model object."""
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('blog-detail', args=[str(self.id)])

class Blogger(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('blogger-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


