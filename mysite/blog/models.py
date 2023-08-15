from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()\
        .filter(status='published')
    

class Post(models.Model):
    """table containing a post data"""
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, 
                            unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='model_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    
    #custom managers
    objects = models.Manager() #default
    published = PublishedManager() #for  published posts

    class Meta:
        ordering = ('-publish',)


    def __str__(self):
        return self.title







