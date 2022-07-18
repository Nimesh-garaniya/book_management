"""book_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from books.views import BookList, BookCreate, BookUpdate, BookDetail, BookAjaxDatatableView

app_name = 'book'

urlpatterns = [
                  path('list/', BookList.as_view(), name="BookList"),
                  path('book-create', BookCreate.as_view(), name="BookCreate"),
                  path('book-update/<int:pk>', BookUpdate.as_view(), name="BookUpdate"),
                  path('book-detail/<int:pk>', BookDetail.as_view(), name="BookDetail"),
                  path('ajax_datatable/books/', BookAjaxDatatableView.as_view(), name="ajax_datatable_books"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
