from .models import Profile,Post,Comment
from django import forms

class DetailsForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['profile','date','like']

# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         # fields = "__all__"
#         exclude = ['user', 'post', 'date', 'count']
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs.update({'autofocus': 'autofocus', 'placeholder': 'Add a comment...'})