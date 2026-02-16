from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Review,Comment,Reply,Post,AnimeStatus,PostReport,ReviewReport,ReplyReport,CommentReport,UserProfile
from django.core.validators import MinValueValidator, MaxValueValidator
class SignUpForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username','email','password1','password2']


    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].validators.extend([MinValueValidator(1),
                                                 MaxValueValidator(10)])
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'comment': forms.HiddenInput(),  # Add a hidden field for storing the comment id
        }
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
class AnimeStatusForm(forms.ModelForm):
    class Meta:
        model = AnimeStatus
        fields = ['status']

    STATUS_CHOICES = [
        ('watched', 'Watched'),
        ('currently-watching', 'Currently Watching'),
        ('plan-to-watch', 'Plan to Watch'),
        ('dropped', 'Dropped'),
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

class PostReportForm(forms.ModelForm):
    class Meta:
        model = PostReport
        fields = ['reason']

# Form for reporting a comment
class CommentReportForm(forms.ModelForm):
    class Meta:
        model = CommentReport
        fields = [ 'reason']

# Form for reporting a reply
class ReplyReportForm(forms.ModelForm):
    class Meta:
        model = ReplyReport
        fields = ['reason']

# Form for reporting a review
class ReviewReportForm(forms.ModelForm):
    class Meta:
        model = ReviewReport
        fields = ['reason']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['description' , 'profile_image_url', 'background_image_url']
