"""habr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from core.views import *


var_gexsalge = "article/<int:id>/hide/"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('sign-in/', sign_in, name='sign_in' ),
    path('sign-out/', sign_out, name='sign_out' ),
    path('register/', register, name="register"),
    path("", index, name='index'),
    path("articles/", articles, name='articles'),
    path("article/<int:id>/", article, name='article'),
    path("authors/", authors, name='authors'),
    path("author/<int:pk>/", author_page, name="author"),
    path("about/", about, name='about'),
    path("article/<int:pk>/edit/", article_edit, name='article_edit'),
    path("article_add/", article_add, name='article_add'),
    path("article/form/", article_form, name='article_form'),
    path("article/<int:id>/delete/", delete_article, name='article-delete'),
    path("top/", top, name='top'),
    path("search/", search, name="search" )

]   + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


