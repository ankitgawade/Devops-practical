from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AniconnectAniDesc(models.Model):
    anime_id = models.IntegerField(db_column='anime_id',primary_key=True)
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase.
    synopsis = models.TextField(db_column='Synopsis', blank=True, null=True)  # Field name made lowercase.
    image_url = models.TextField(db_column='Image_Url', blank=True, null=True)  # Field name made lowercase.
    genres = models.TextField(db_column='Genres', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'aniconnect_ani_desc'

class Category(models.Model):
    title = models.CharField(max_length=50)

class Review(models.Model):
    anime = models.ForeignKey(AniconnectAniDesc, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you have a User model
    rating = models.IntegerField()  # You can define your rating system here
    comment = models.TextField()

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Default to the first category
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='post_dislikes', blank=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class AnimeStatus(models.Model):
    STATUS_CHOICES = [
        ('watched', 'Watched'),
        ('currently-watching', 'Currently Watching'),
        ('plan-to-watch', 'Plan to Watch'),
        ('dropped', 'Dropped'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey( AniconnectAniDesc, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

class BaseReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    reviewed = models.BooleanField(default=False)

    class Meta:
        abstract = True

# Report model for reported posts
class PostReport(BaseReport):
    reported_post = models.ForeignKey('Post', on_delete=models.CASCADE)

# Report model for reported comments
class CommentReport(BaseReport):
    reported_comment = models.ForeignKey('Comment', on_delete=models.CASCADE)

# Report model for reported replies
class ReplyReport(BaseReport):
    reported_reply = models.ForeignKey('Reply', on_delete=models.CASCADE)

# Report model for reported reviews
class ReviewReport(BaseReport):
    reported_review = models.ForeignKey('Review', on_delete=models.CASCADE)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField()
    profile_image_url = models.URLField(blank=True, null=True, max_length=300)
    background_image_url = models.URLField(blank=True, null=True ,max_length=300) 

    def __str__(self):
        return self.user.username + "'s Profile"
