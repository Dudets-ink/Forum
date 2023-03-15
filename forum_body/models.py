from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    """Discussion"""

    name = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

class Discuss(models.Model):
    """Branch of discussion"""

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    head = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.head

class Messages(models.Model):
    """Message in branch of discussion"""

    discuss = models.ForeignKey(Discuss, on_delete=models.CASCADE) 
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=20000)


