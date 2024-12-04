from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.utils import timezone
from django.core.paginator import Paginator
from blog.models import Post, Category

now = timezone.now()
paginator_pages = 5

def index(request):
    template_name = 'blog/index.html'
    postsbd = Post.objects.filter(
        pub_date__lte=now,
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')
    paginator = Paginator(postsbd, paginator_pages)
    page = paginator.get_page(request.GET.get('page'))
    context = {'page': page}
    return render(request, template_name, context)

def post_detail(request, id):
    template_name = 'blog/detail.html'
    post = get_object_or_404(Post, id=id)
    if post.pub_date > timezone.now():
        raise Http404("Публикация еще не доступна.")
    elif not post.is_published:
        raise Http404("Публикация не найдена или не опубликована.")
    elif not post.category.is_published:
        raise Http404("Категория публикации не найдена или не опубликована.")
    context = {'post': post}
    return render(request, template_name, context)


def category_posts(request, category_slug):
    template_name = 'blog/category.html'
    category = get_object_or_404(Category, slug=category_slug)
    if not category.is_published:
        raise Http404("Категория не найдена или не опубликована.")
    postsbd = Post.objects.filter(
        category=category,
        pub_date__lte=now,
        is_published=True,
        )
    context = {
        'postsbd': postsbd,
        'category': category,  
    }
    return render(request, template_name, context)
