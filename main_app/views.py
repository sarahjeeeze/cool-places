from django.shortcuts import render
from .models import Post, Profile, Comment
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm
from jinja2 import Template
from .forms import CustomUserCreationForm  
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UpdateUserForm, UpdateProfileForm, CommentForm
from django.contrib.auth.models import User
from .models import Profile


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        try:
            profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        except: 
            profile_form = UpdateProfileForm(request.POST, request.FILES)
        if user_form.is_valid():
            try:
                user_form.save()
            except:
                pass
        if profile_form.is_valid():
            try:
                profile_form.save()
            except Exception as e:
                pass
            messages.success(request, 'Your profile is updated successfully')
            return redirect('profile')
    else:
        try:
            user_form = UpdateUserForm(instance=request.user)
        except:
            user_form = UpdateUserForm()
        try:
            profile_form = UpdateProfileForm(instance=request.user.profile)
        except:
            profile_form = UpdateProfileForm()

    return render(request, 'main_app/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def profile(request):
    profile = get_object_or_404(User, username=request.user)
    try:
        more_profile = get_object_or_404(Profile, username=request.user)
    except Exception as e:
        more_profile = "No avatar or Bio yet."
    return render(request, 'main_app/profile.html', {'profile': profile, 'more': more_profile})

def another_profile(request, pk):
    more_profile = get_object_or_404(Profile, pk=pk)
    return render(request, 'main_app/another_profile.html', {'profile': profile, 'more': more_profile})


def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Registration successful. You can now login")
			return render (request=request, template_name="registration/register.html", context={"register_form":form})
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="registration/register.html", context={"register_form":form})

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def post_list(request):
    posts = {}
    try:
        posts = Post.objects.all()
    except Exception:
        pass
    return render(request, 'main_app/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    likes = get_object_or_404(Post,pk=pk).likes.count()
    return render(request, 'main_app/post_detail.html', {'post': post, 'likes': likes})

def post_new(request):
    if request.method == 'POST':
        updated_request = request.POST.copy()
        updated_request['profile'] = str(request.user.profile.pk)
        form = PostForm(updated_request, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    mapbox_access_token = "'pk.eyJ1Ijoic2dyaWZmaXRoczEyIiwiYSI6ImNsNDMzdGo4ZDB4em4za282cmJhemFka24ifQ.m4ufhKsweS1MWLuCvNigvA'"
    return render(request, 'main_app/post_edit.html', {'form': form, 'mapbox_access_token': mapbox_access_token})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'main_app/post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('published_date')
    return render(request, 'main_app/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('main_app/post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('main_app/post_list')

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'main_app/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def post_map(request):
    posts = Post.objects.all()
    all_posts = [] 
    template = Template("""{
      type: 'Feature',
      geometry: {
        type: 'Point',
        coordinates: [{{long}}, {{lat}}]
      },
      properties: {
        title: '{{ location }}',
        image: '{{ image_address }}',
        link: '{{ pk }}'
      }
    }""")
    for value in posts:
        image = value.main_image.url
        lat = value.location[0]
        long = value.location[1]
        location = value.place_name
        key = value.pk
        link = "<a href=""/post/{}"">".format(key)
        temp = template.render(image_address = image, long=long, lat=lat, location=location, pk=link)
        all_posts.append(temp)
    posts = ','.join(all_posts)
    mapbox_access_token = "'pk.eyJ1Ijoic2dyaWZmaXRoczEyIiwiYSI6ImNsNDMzdGo4ZDB4em4za282cmJhemFka24ifQ.m4ufhKsweS1MWLuCvNigvA'"
    return render(request, 'main_app/post_map.html', {'posts': posts, 'mapbox_access_token': mapbox_access_token})