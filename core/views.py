from django.shortcuts import render, redirect
from .models import Post, User
from .forms import PostForm


def dashboard_view(request):
    recent_posts = Post.objects.order_by('-created_at')[:3]
    return render(request, 'core/dashboard.html', {
        'recent_posts': recent_posts
    })


def community_view(request):
    posts = Post.objects.order_by('-created_at')
    form = PostForm()
    return render(request, 'core/community.html', {
        'posts': posts,
        'form': form
    })


def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = User.objects.first()  # tijdelijk
            post.save()
            return redirect('community')
    return redirect('community')


def zoeken_view(request):
    return render(request, 'core/zoeken.html')


def profiel_view(request):
    return render(request, 'core/profiel.html')