from django.contrib import admin

from books.models import Author, Book, Comment


class AuthorAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]


class BookAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'author_id',
        'price',
        'founded_on',
        'file',
        'front_pic',
        'book_desc',
    ]


class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'book',
        'name',
        'email',
        'rating',
        'body',
    ]


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Comment, CommentAdmin)
