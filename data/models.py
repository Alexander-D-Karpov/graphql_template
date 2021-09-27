from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    user = models.ManyToManyField(User)
    body = models.TextField()

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title