from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, User, Institution
from .forms import PostForm, UserRegistrationForm, UserEditForm


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


@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Post succesvol aangemaakt!')
            return redirect('community')
    return redirect('community')


def zoeken_view(request):
    return render(request, 'core/zoeken.html')


@login_required
def profiel_view(request):
    return render(request, 'core/profiel.html')


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profiel succesvol bijgewerkt!')
            return redirect('profiel')
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'core/edit_profile.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account succesvol aangemaakt! Je kunt nu inloggen.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'core/register.html', {'form': form})