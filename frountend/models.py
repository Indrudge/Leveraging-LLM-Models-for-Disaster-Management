# Create your models here.
from djongo import models

class NewsArticle(models.Model):
    title = models.TextField()
    description = models.TextField()
    date = models.DateTimeField()
    url = models.URLField(unique=True)
    content = models.TextField()

    def __str__(self):
        return self.title
