from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    author = models.ForeignKey(User, verbose_name="Author", on_delete=models.CASCADE)
    title = models.CharField("", max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_checked = models.BooleanField(default=False)
