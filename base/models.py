from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Task(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    CATEGORY_CHOICES = (
        ('İş', 'İş'),
        ('Gezi', 'Gezi'),
        ('Kişisel', 'Kişisel'),
    )
    category = models.CharField(null=True, max_length=10, choices=CATEGORY_CHOICES)
    objects = models.Manager()
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

    class Meta:
        order_with_respect_to = 'user'

def get_todos():
    return Task.objects.filter(is_deleted=False)