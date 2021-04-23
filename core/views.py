from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse

from core.models import *
from core.forms import ArticleForm
from .filters import ArticleFilter

from django.db.models import Q

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required

from django.views.generic import TemplateView

User = get_user_model()

def index(request):
    return render(request, "index.html")

def articles(request):
    article_filter = ArticleFilter(request.GET, queryset=Article.objects.filter(is_active=True))
    return render(
        request,
        "articles.html",
        {"article_filter": article_filter}
    )

def authors(request):
    authors = Author.objects.all()
    return render(
        request,
        "authors.html",
        {"authors": authors}
        )

def author_page(request, pk):
    author = Author.objects.get(pk=pk)
    return render(
        request,
        "author.html",
        {"author":author})

def article(request, id):
    article = Article.objects.get(id=id)
    article.views += 1
    article.save()
    return render(
        request,
        "article_page.html",
        {"article" : article }
        )


def top(request):
    articles = Article.objects.filter(is_active=True).order_by("-views", "pk")[:3]
    return render(request, "articles.html", {"articles":articles})


def about(request):
    return render(request, "about.html")

def article_edit(request, pk):
    article = Article.objects.get(id=pk)

    if request.method == "POST":
        article.title = request.POST.get("title")
        article.text = request.POST.get("text")
        article.save()
        return redirect(article_page, pk)
    return render(request, "article_edit.html", {"article": article})

@login_required(login_url='/sign-in/')
def article_add(request):
    if 'title' in request.POST and 'text' in request.POST: 
        title = request.POST["title"]
        text = request.POST["text"]
        img = request.FILES.get("img")
        article = Article(title=title, text=text, img=img)
        user = request.user
        article.save()

        if not Author.objects.filter(user=user):
            author = Author(user=user, nickname=user.username)
            author.save()

        
        
        return redirect(articles)


    return render(
        request, 
        "article_add.html", 
        )
def article_form(request):
    context = {}

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article_obj = form.save()
            return redirect(article, article_obj.id)

    form = ArticleForm()
    context['form'] = form
    return render(request, 'form.html', context)

def delete_article(request, id):
    article = Article.objects.get(pk=id)
    article.delete()
    return HttpResponse("Статья была удалена")

def search(request):
    word = request.GET.get("word")
    articles = Article.objects.filter(
        Q(title__icontains=word) | Q(text__icontains=word), 
        is_active=True) # Типа лайка
    return render(request, "articles.html", {"articles": articles})

def sign_in(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('index')
    else:
        return render(request, 'sign_in.html')


def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password != password2:
            return render(request, 'register.html', {'message': 'Пароли не совпадают!'})
        elif User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'message': 'Логин уже используется'})
        else:
            User.objects.create_user(
                username=username,
                password=password,
            )
            return redirect(sign_in)


def sign_out(request):
    logout(request)
    return redirect(sign_in)

def sign_up(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            if user.is_active:
                login(request, user)
                return redirect('index')
        else:
            return render(request, 'sign_in.html')

    