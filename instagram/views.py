from typing_extensions import Self
from django.shortcuts import get_object_or_404, render,redirect
from django.http  import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import ListView
from .models import Follower, Likes, Profile,Post,Following,Comment
from .forms import CommentForm, DetailsForm,PostForm
from django.db.models import F
from django.db.models import Q

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

@login_required(login_url='/accounts/login/')
def timeline(request):
    users = User.objects.all()
    posts = Post.objects.all()
    follows = Following.objects.all()
    comments = Comment.objects.all()

    if request.method=='POST' and 'follow' in request.POST:
        following=Following(username=request.POST.get("follow"),followed=request.user.username)
        following.save()
        return redirect('timeline')
    elif request.method=='POST' and 'comment' in request.POST:
        comment=Comment(comment=request.POST.get("comment"),
                        post=int(request.POST.get("posted")),
                        username=request.POST.get("user"),
                        count=0)
        comment.save()
        comment.count=F('count')+1
        return redirect('timeline')
    elif request.method=='POST' and 'post' in request.POST:
        posted=request.POST.get("post")
        for post in posts:
            if (int(post.id)==int(posted)):
                post.like+=1
                post.save()
        return redirect('timeline')
    else:
        return render(request, 'timeline.html',{"users":users,"follows":follows,"posts":posts,"comments":comments})

@login_required(login_url='/accounts/login/')
def edit_profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = DetailsForm(request.POST, request.FILES)
        if form.is_valid():
                Profile.objects.filter(id=current_user.profile.id).update(bio=form.cleaned_data["bio"])
                profile = Profile.objects.filter(id=current_user.profile.id).first()
                profile.profile_pic.delete()
                profile.profile_pic=form.cleaned_data["profile_pic"]
                profile.save()
        return redirect('profile')

    else:
        form = DetailsForm()
    
    return render(request, 'edit_profile.html',{"form": form})

@login_required(login_url='/accounts/login/')
def other_profile(request,id):
    profile_user=User.objects.filter(id=id).first()
    posts=Post.objects.all()
    following=Following.objects.filter(username=profile_user.username).all()
    followingcount=len(following)
    followers=Following.objects.filter(followed=profile_user.username).all()
    followercount=len(followers)
    return render(request, 'other_profile.html',{"profile_user": profile_user,"posts":posts,"followingcount":followingcount,"followercount":followercount})

@login_required(login_url='/accounts/login/')
def search(request):
    posts=Post.objects.all()
    if 'username' in request.GET and request.GET["username"]:
        search_term = request.GET.get("username")
        following=Following.objects.filter(username=search_term).all()
        followingcount=len(following)
        followers=Following.objects.filter(followed=search_term).all()
        followercount=len(followers)
        searched_user = User.objects.filter(username=search_term).first()
        if searched_user:
            message = f"{search_term}"
            return render(request, 'other_profile.html',{"profile_user": searched_user,"posts":posts,"followingcount":followingcount,"followercount":followercount})
        else:
            message = "The username you are searching for does not exist."
            return render(request, 'notfound.html',{"message":message})

def like_post(request, post_id):
    post = get_object_or_404(Post,id = post_id)
    like = Likes.objects.filter(post = post ,user = request.user).first()
    if like is None:
        like = Likes()
        like.post = post
        like.user = request.user
        like.save()
    else:
        like.delete()
    return redirect('timeline')  

def single_comment(request, post_id):
    post = get_object_or_404(Post,id = post_id)
    # comment = Comment.objects.filter(post = post ,user = request.id).first()
    comment=Comment.objects.filter(post=post).all()
    current_user=request.user

    if request.method =='POST':
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = current_user
            
            comment.post = post
            comment.save()
        return redirect('timeline')
    else:
        
        form = CommentForm()
    return render(request, 'comment.html', {'post': post, 'form':form, 'comment':comment})  


def follow(request):
    if request.method == 'GET':
        user_id = request.GET['user_id']
        usertofollow = User.objects.get(pk=user_id)  # getting the user to follow

        if Follower.objects.filter(being_followed=usertofollow, follower=request.user).exists():
            Follower.objects.filter(being_followed=usertofollow, follower=request.user).delete()
        else:
            m = Follower(being_followed=usertofollow, follower=request.user)  # creating like object
            m.save()  # saves into database
        return HttpResponse(usertofollow.being_followeds.count())
    else:
        return HttpResponse("Request method is not a GET")
        
class FollowerListView(LoginRequiredMixin, ListView):
    model = Follower

    def get_queryset(self):
        # org qs
        qs = super().get_queryset()
        # filter by var from captured url
        return qs.filter(Q(follower__username=self.kwargs['username']) | Q(being_followed__username=self.kwargs['username']))