import datetime

from django.db import models

from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=120, verbose_name="Book Name", unique=True)
    author_id = models.ForeignKey(Author, verbose_name="Book Author", on_delete=models.CASCADE, null=True)
    price = models.PositiveIntegerField(verbose_name="Price", validators=[MinValueValidator(1)])
    founded_on = models.DateField(verbose_name="Founded Date", validators=[MaxValueValidator(datetime.date.today)])
    file = models.FileField(upload_to='book-pdf/ %Y/ %m/ %d/', validators=[FileExtensionValidator(['pdf'])])
    front_pic = models.ImageField(upload_to='images/', verbose_name="Book Image", validators=[FileExtensionValidator(['jpeg', 'jpg'])])
    book_desc = models.TextField(verbose_name="About")

    # create_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# comment model
class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=50)
    email = models.EmailField()
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    rate_choices = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10)
    )
    rating = models.IntegerField(choices=rate_choices, verbose_name="Rate Book")
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.name

    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)
