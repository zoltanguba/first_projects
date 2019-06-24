from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings


class Translate(models.Model):
    library = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    language = models.CharField(max_length=5)
    content = models.TextField(max_length=2000)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=1
    )

    def __str__(self):
        return self.title


# redirect the page to the newly created post's url after the post is created
    def get_absolute_url(self):
        return reverse('contentlist')


class WordDatabase(models.Model):
    srcLanguage = models.CharField(max_length=5)
    word = models.CharField(max_length=100)
    destLanguage = models.CharField(max_length=5)
    translatedWord1 = models.CharField(max_length=100)
    translatedWord2 = models.CharField(max_length=100)
    translatedWord3 = models.CharField(max_length=100)
    knownlevel = models.CharField(max_length=10, default=1)
    contentid = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )


class DestinationLanguage(models.Model):
    destLanguage = models.CharField(max_length=5, default='EN')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )