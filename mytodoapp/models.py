from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    closed = models.BooleanField(default=False)
    created_date = models.DateTimeField("date created")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return "{}: '{}'".format(self.author, self.title)
    def to_dict(self):
        return {"id": self.id,
                "title": self.title,
                "description": self.description,
                "closed": self.closed,
                "created_date": self.created_date,
                "author": self.author.username,
                "author_id": self.author.id}
