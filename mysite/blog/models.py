from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Post(models.Model):
    # Status attribute for knowing status of posts (post is ready for publishing, or draft post maybe will be updated)
    class Status(models.TextChoices):
       DRAFT = 'DF', 'Draft'
       PUBLISHED = 'PB' , 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    #One to many relationship
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,choices=Status.choices,default=Status.DRAFT)
    
    # This class for creating default sort ordering, the way we want posts are displayed
    class Meta:
      # We added hyphen for ordering from newer to older if the ordering is not specified
      ordering = ['-publish']
      # For improving quiery's speed 
      indexes =  [models.Index(fields=['-publish'])]
    # gives the class title readable on the front of the site, you can put 'body' attribute instead of 'title' 
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("blog:post_details", args=[self.id])
class Comment(models.Model):
    post  = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
    name  = models.CharField(max_length=80) 
    email = models.EmailField()
    body  = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active  = models.BooleanField(default=True)
    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]
        def __str__(self):
            return f'Comment by {self.name} on {self.post}'
            
        