from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    options = (
        ('d', 'Draft'),
        ('p', 'Published')
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.URLField(max_length=5000, blank=True)
    published_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=options, default='draft')
    slug = models.SlugField(blank=True, unique=True)
    
    def __str__(self):
        return self.title

