from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # profile_pic = models.ImageField(blank=True,upload_to = 'images/')
    profile_pic = CloudinaryField('image')
    bio = models.CharField(max_length = 255)

    def __str__(self):
        return f'{self.user.username}'

class Post(models.Model):
    # pic = models.ImageField(upload_to = 'posts/')
    pic = CloudinaryField('image')
    caption = models.CharField(blank=True,max_length = 255)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    like = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.profile.user.username}'

class Following(models.Model):
    username = models.CharField(blank=True,max_length = 255)
    followed = models.CharField(blank=True,max_length = 255)

    def __str__(self):
        return f'{self.username}'

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.username}'

class Likes(models.Model):
    post = models.ForeignKey(Post,related_name='like_count', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.post
    def save_likes(self):
        self.save()

    # update like
    def update_likes(self, name):
        self.name = name
        self.save()

     # delete like from database
    def delete_likes(self):
        self.delete()
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name="unique_like"),
        ] 
class Follower(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    being_followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='being_followeds')

    def __str__(self):
        return f'{self.follower.user, self.being_followed.user} follower-> followee'
    





