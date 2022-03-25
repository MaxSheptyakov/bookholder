from django.db import models
from django.urls import reverse


class Book(models.Model):
    title = models.CharField(max_length=255, )
    author = models.CharField(max_length=1023, null=True)
    description = models.TextField()
    url = models.URLField(null=True)
    slug = models.SlugField(null=True)

    def get_absolute_url(self):
        return reverse('book_receiver:book_info', args=[self.slug])

    def __str__(self):
        return f'Book "{self.title}".\nDescription: {self.description}'


class BookType(models.Model):
    TYPE_CHOICES = (
        ('FN', 'Фантастика'),
        ('SF', 'Научпоп'),
        ('IT', 'IT'),
        ('CL', 'Классика')
    )
    book_type = models.CharField(choices=TYPE_CHOICES, max_length=2, blank=False, primary_key=True, null=False)
    books = models.ManyToManyField(Book, related_name='book_types')

    class Meta:
        ordering=['book_type']

    def __str__(self):
        return self.book_type