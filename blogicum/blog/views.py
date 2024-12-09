from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.utils import timezone
from django.core.paginator import Paginator
from blog.models import Post, Category
from django.shortcuts import render, redirect
from .forms import PostForm, PostEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm

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



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('blog:index')
    else:
        form = LoginForm()
    return render(request, 'blog/login.html', {'form': form})

def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:login')
    else:
        form = RegistrationForm()
    return render(request, 'blog/registration.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('blog:index')



def add_post(request):
    if not request.user.is_authenticated:
        return redirect('blog:login')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, user=request.user)
        form.request = request
        if form.is_valid():
            form.save()
            return redirect('blog:index')
    else:
        form = PostForm()
    return render(request, 'blog/add_post.html', {'form': form})

@login_required
def post_edit(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author != request.user:
        return redirect('blog:index')
    if request.method == 'POST':
        form = PostEditForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', id=id)
    else:
        form = PostEditForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author != request.user:
        return redirect('blog:index')
    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')
    return redirect('blog:index')