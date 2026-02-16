from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('anime_page/<int:anime_id>/', views.anime_page, name='anime_page'),
    path('forum_head/', views.forum_head, name='forum_head'),
    path('forum_detail/<int:id>/', views.forum_detail, name='forum_detail'),
    path('forum_post/<int:id>/', views.forum_post, name='forum_post'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/dislike/', views.dislike_post, name='dislike_post'),
    path('reported_reviews/', views.reported_reviews, name='reported_reviews'),
    path('remove_review/', views.remove_review, name='remove_review'),
    path('remove_post/', views.remove_post, name='remove_post'),
    path('remove_comment/', views.remove_comment, name='remove_comment'),
    path('remove_reply/', views.remove_reply, name='remove_reply'),
    path('search/', views.search, name='search'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]
