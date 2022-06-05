from django.shortcuts import render,redirect
from django.http  import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile,Post,Following,Comment
from .forms import DetailsForm,PostForm
from django.db.models import F

# Create your views here.
def welcome(request):

    return render(request, 'welcome.html')

@login_required(login_url='/accounts/login/')
def profile(request):
    posts=Post.objects.all()
    current_user = request.user
    following=Following.objects.filter(username=current_user.username).all()
    followingcount=len(following)
    followers=Following.objects.filter(followed=request.user.username).all()
    followercount=len(followers)
    if request.method == 'POST':
        form = DetailsForm(request.POST, request.FILES)
        form1 = PostForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()

        if form1.is_valid():
            post = form1.save(commit=False)
            post.profile = current_user.profile
            post.save()

        return redirect('profile')

    else:
        form = DetailsForm()
        form1 = PostForm()
    
    return render(request, 'profile.html', {"form":form,"form1":form1,"posts":posts,"followingcount":followingcount,"followercount":followercount})

    
