from django.db import models


class Movie(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=300, blank=False)
    director = models.CharField(max_length=500, blank=True, null=True)
    genre = models.CharField(max_length=2000, blank=True, null=True)
    metascore = models.IntegerField(null=True)

    class Meta:
        ordering = ('created',)


class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField(blank=False)
    movie_id = models.ForeignKey(Movie, related_name='comments', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)
