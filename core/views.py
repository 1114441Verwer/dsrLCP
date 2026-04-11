from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Post, User, Institution
from .forms import PostForm, UserRegistrationForm, UserEditForm
import re


def dashboard_view(request):
    recent_posts = Post.objects.order_by('-created_at')[:3]
    
    # Split categories and target_audience for template rendering
    for post in recent_posts:
        if post.category:
            post.category_list = [cat.strip() for cat in post.category.split(',')]
        else:
            post.category_list = []
        if post.target_audience:
            post.audience_list = [aud.strip() for aud in post.target_audience.split(',')]
        else:
            post.audience_list = []
    
    form = PostForm()
    return render(request, 'core/dashboard.html', {
        'recent_posts': recent_posts,
        'form': form
    })


def community_view(request):
    posts = Post.objects.order_by('-created_at')
    
    # Split categories and target_audience for template rendering
    for post in posts:
        if post.category:
            post.category_list = [cat.strip() for cat in post.category.split(',')]
        else:
            post.category_list = []
        if post.target_audience:
            post.audience_list = [aud.strip() for aud in post.target_audience.split(',')]
        else:
            post.audience_list = []
    
    # Get top contributors (users with most points)
    top_users = User.objects.filter(points__gt=0).order_by('-points')[:4]
    
    # Get popular categories
    from collections import Counter
    all_categories = []
    for post in posts:
        if post.category_list:
            all_categories.extend(post.category_list)
    popular_categories = [cat for cat, count in Counter(all_categories).most_common(6)]
    
    form = PostForm()
    return render(request, 'core/community.html', {
        'posts': posts,
        'form': form,
        'top_users': top_users,
        'popular_categories': popular_categories,
        'total_users': User.objects.count(),
        'active_discussions': posts.count(),
    })


@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            # Combine multiple categories with comma separator
            if 'category' in form.cleaned_data:
                categories = form.cleaned_data['category']
                if isinstance(categories, list):
                    post.category = ', '.join(categories)
                else:
                    post.category = categories
            # Combine multiple target audiences with comma separator
            if 'target_audience' in form.cleaned_data:
                audiences = form.cleaned_data['target_audience']
                if isinstance(audiences, list):
                    post.target_audience = ', '.join(audiences)
                else:
                    post.target_audience = audiences
            post.save()
            
            # Add points for posting
            request.user.points += 100
            request.user.save()
            
            messages.success(request, 'Post succesvol aangemaakt! +100 punten 🎉')
            return redirect('community')
    return redirect('community')


@login_required
def edit_post_view(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        messages.error(request, 'Post niet gevonden.')
        return redirect('community')
    
    # Check if user is the author
    if post.user != request.user:
        messages.error(request, 'Je bent niet bevoegd om deze post te bewerken.')
        return redirect('community')
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            # Combine multiple categories with comma separator
            if 'category' in form.cleaned_data:
                categories = form.cleaned_data['category']
                if isinstance(categories, list):
                    post.category = ', '.join(categories)
                else:
                    post.category = categories
            # Combine multiple target audiences with comma separator
            if 'target_audience' in form.cleaned_data:
                audiences = form.cleaned_data['target_audience']
                if isinstance(audiences, list):
                    post.target_audience = ', '.join(audiences)
                else:
                    post.target_audience = audiences
            post.save()
            messages.success(request, 'Post succesvol bijgewerkt!')
            return redirect('community')
    else:
        form = PostForm(instance=post)
    
    return render(request, 'core/edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post_view(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        messages.error(request, 'Post niet gevonden.')
        return redirect('community')
    
    # Check if user is the author
    if post.user != request.user:
        messages.error(request, 'Je bent niet bevoegd om deze post te verwijderen.')
        return redirect('community')
    
    if request.method == 'POST':
        post_title = post.title
        post.delete()
        messages.success(request, f'Post "{post_title}" succesvol verwijderd!')
        return redirect('community')
    
    return render(request, 'core/delete_post.html', {'post': post})


def zoeken_view(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    post_type = request.GET.get('type', '').strip()

    posts = []
    users = []
    institutions = []

    # Als categorie Instelling is: alleen instellingen zoeken
    if category == 'Instelling':
        institutions = Institution.objects.all()
        if query:
            institutions = institutions.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )

    # Als categorie Persoon is: alleen personen zoeken
    elif category == 'Persoon':
        users = User.objects.all()
        if query:
            users = users.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(function__icontains=query)
            )

    # Anders: posts zoeken (+ eventueel personen/instellingen als er een query is)
    else:
        posts = Post.objects.all().order_by('-created_at')

        if query:
            posts = posts.filter(
                Q(title__icontains=query) |
                Q(short_description__icontains=query) |
                Q(long_description__icontains=query) |
                Q(user__username__icontains=query)
            )

        # Filter op categorie
        if category and category != 'all':
            posts = posts.filter(category__icontains=category)

        # Filter op type
        if post_type and post_type != 'all':
            posts = posts.filter(type__iexact=post_type)

        # Bij een query zonder specifieke categorie: ook personen en instellingen zoeken
        if query and (not category or category == 'all'):
            users = User.objects.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(function__icontains=query)
            )
            institutions = Institution.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )

    # Split categories en target_audience voor template rendering
    for post in posts:
        if post.category:
            post.category_list = [cat.strip() for cat in post.category.split(',')]
        else:
            post.category_list = []
        if post.target_audience:
            post.audience_list = [aud.strip() for aud in post.target_audience.split(',')]
        else:
            post.audience_list = []

    # Bereken totaal resultaten
    from django.db.models import QuerySet
    posts_count = posts.count() if isinstance(posts, QuerySet) else len(posts)
    users_count = users.count() if isinstance(users, QuerySet) else len(users)
    inst_count = institutions.count() if isinstance(institutions, QuerySet) else len(institutions)
    results_count = posts_count + users_count + inst_count

    form = PostForm()
    return render(request, 'core/zoeken.html', {
        'posts': posts,
        'users': users,
        'institutions': institutions,
        'query': query,
        'results_count': results_count,
        'form': form,
        'post_type': post_type,
        'category': category
    })


@login_required
def profiel_view(request):
    user_posts = request.user.posts.all().order_by('-created_at')
    
    # Split categories and target_audience for template rendering
    for post in user_posts:
        if post.category:
            post.category_list = [cat.strip() for cat in post.category.split(',')]
        else:
            post.category_list = []
        if post.target_audience:
            post.audience_list = [aud.strip() for aud in post.target_audience.split(',')]
        else:
            post.audience_list = []
    
    form = PostForm()
    return render(request, 'core/profiel.html', {
        'user_posts': user_posts,
        'form': form,
        'is_own_profile': True
    })


def user_profile_view(request, username):
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request, 'Gebruiker niet gevonden.')
        return redirect('zoeken')
    
    user_posts = profile_user.posts.all().order_by('-created_at')
    
    # Split categories and target_audience for template rendering
    for post in user_posts:
        if post.category:
            post.category_list = [cat.strip() for cat in post.category.split(',')]
        else:
            post.category_list = []
        if post.target_audience:
            post.audience_list = [aud.strip() for aud in post.target_audience.split(',')]
        else:
            post.audience_list = []
    
    form = PostForm()
    return render(request, 'core/profiel.html', {
        'user': profile_user,
        'user_posts': user_posts,
        'form': form,
        'is_own_profile': request.user.is_authenticated and request.user == profile_user
    })


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        edit_form = UserEditForm(request.POST, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, 'Profiel succesvol bijgewerkt!')
            return redirect('profiel')
    else:
        edit_form = UserEditForm(instance=request.user)
    
    form = PostForm()
    return render(request, 'core/edit_profile.html', {'edit_form': edit_form, 'form': form})


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