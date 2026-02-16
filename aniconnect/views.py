from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm,ReviewForm,PostForm,CommentForm,ReplyForm,AnimeStatusForm,ReviewReportForm,PostReportForm,CommentReportForm,ReplyReportForm,UserProfileForm
from .models import AniconnectAniDesc,Review,Category,Post,Comment,Reply,AnimeStatus,ReviewReport,PostReport,CommentReport,ReplyReport,UserProfile
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
@csrf_exempt

def edit_profile(request):
	try:
		profile = UserProfile.objects.get(user=request.user)
	except UserProfile.DoesNotExist:
        # If the profile does not exist, create a new one
		profile = UserProfile(user=request.user)
    
	if request.method == 'POST':
		form = UserProfileForm(request.POST, instance=profile)
		if form.is_valid():
			form.save()
			return redirect('home')  # Redirect to the home page after saving
	else:
		form = UserProfileForm(instance=profile)
	return render(request, 'edit_profile.html', {'form': form})


def search(request):
	if request.method == 'POST':
		searched=request.POST['searched']
		animes=AniconnectAniDesc.objects.filter(name__contains=searched)
		return render(request, 'search.html',{'animes':animes, 'searched':searched})
	else:
		return render(request, 'search.html', {})

def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, "Login Error")
            return redirect('home')

    else:
        animes = AniconnectAniDesc.objects.all()[:20]  # first 20
        return render(request, 'home.html', {'animes': animes})


def logout_user(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out...")
	return redirect('home')

def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('home')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})

	return render(request, 'register.html', {'form':form})

def anime_page(request,anime_id):
	anime = get_object_or_404(AniconnectAniDesc, pk=anime_id)
	reviews = Review.objects.filter(anime=anime)
	review_form = ReviewForm()
	status_form = AnimeStatusForm()
	review_report_form = ReviewReportForm() 
	if request.method == 'POST':
		if 'review-submit' in request.POST:
			review_form = ReviewForm(request.POST)
			if review_form.is_valid():
				review = review_form.save(commit=False)
				review.anime = anime
				review.user = request.user
				review.save()
				return redirect('anime_page', anime_id=anime_id)
			else:
				review_form = ReviewForm()
				return render(request, 'anime_page.html', {'anime': anime, 'reviews': reviews, 'review_form': review_form,'status_form': status_form,'review_report_form': review_report_form})
		elif 'status-submit' in request.POST:
			status_form = AnimeStatusForm(request.POST)
			if status_form.is_valid():
				status_data = status_form.cleaned_data
				anime_status = AnimeStatus.objects.filter(user=request.user, anime=anime).first()
				if anime_status:
                # If the record exists, update it
					anime_status.status = status_data['status']
					anime_status.save()
				else:
                # If the record doesn't exist, create a new one
					anime_status = AnimeStatus.objects.create(user=request.user, anime=anime, status=status_data['status'])
				return redirect('anime_page', anime_id=anime_id)
			else:
				status_form = AnimeStatusForm()
				return render(request, 'anime_page.html', {'anime': anime, 'reviews': reviews, 'review_form': review_form,'status_form': status_form,'review_report_form': review_report_form})
		elif 'report-submit' in request.POST:  # Handle review report form submission
			review_report_form = ReviewReportForm(request.POST)
			if review_report_form.is_valid():
				report = review_report_form.save(commit=False)
				report.reported_review = get_object_or_404(Review, pk=request.POST.get('review_id'))
				report.user = request.user
				report.save()
				return redirect('anime_page', anime_id=anime_id)
			else:
				review_report_form = review_report_form()
				return render(request, 'anime_page.html', {'anime': anime, 'reviews': reviews, 'review_form': review_form,
											   'status_form': status_form,'review_report_form': review_report_form})
	return render(request, 'anime_page.html', {'anime': anime, 'reviews': reviews, 'review_form': review_form,'status_form': status_form,'review_report_form': review_report_form})

def forum_head(request):
	categories = Category.objects.all()
	return render(request, 'forum_head.html', {'categories':categories})

def forum_detail(request,id):
	category = get_object_or_404(Category, pk=id)
	Posts= Post.objects.filter(category=category)
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.category=category
			post.author=request.user
			post.save()
			return redirect('forum_detail', id=id)
	else:
		form = PostForm()
		return render(request, 'forum_detail.html', {'category': category,'Posts': Posts, 'form': form,})
	

def forum_post(request,id):
	post = get_object_or_404(Post, pk=id)
	Comments= Comment.objects.filter(post=post)
	comment_form=CommentForm()
	reply_form = ReplyForm()
	post_report_form=PostReportForm()
	replies = Reply.objects.filter(comment__in=Comments)
	comment_report_form=CommentReportForm()
	reply_report_form=ReplyReportForm()
	comment_replies = {}
	for comment in Comments:
		comment_replies[comment.id] = comment.replies.all()
	context={'Comments':Comments,'comment_replies':comment_replies,'replies':replies,'post':post,
			'comment_form': comment_form,'reply_form':reply_form,'post_report_form':post_report_form,
			'comment_report_form':comment_report_form,'reply_report_form':reply_report_form}
	if request.method == 'POST':
		if 'comment-submit' in request.POST:
			comment_form = CommentForm(request.POST)
			if comment_form.is_valid():
				new_comment = comment_form.save(commit=False)
				new_comment.post = post
				new_comment.author = request.user
				new_comment.save()
				return redirect('forum_post', id=id)
			else:
				comment_form = CommentForm()
				return render(request, 'forum_post.html', context)
		elif 'reply-submit' in request.POST:  # Handling reply submission
			reply_form = ReplyForm(request.POST)
			if reply_form.is_valid():
				reply = reply_form.save(commit=False)
				comment_id = request.POST.get('comment_id')
				comment = get_object_or_404(Comment, pk=comment_id)
				reply.comment = comment
				reply.author = request.user
				reply.save()
				return redirect('forum_post', id=id)
			else:
				reply_form =reply_form ()
				return render(request, 'forum_post.html',context)
		elif 'report-post-submit' in request.POST:  # Handle review report form submission
			post_report_form = PostReportForm(request.POST)
			if post_report_form.is_valid():
				report = post_report_form.save(commit=False)
				report.reported_post = get_object_or_404(Post, pk=request.POST.get('post_id'))
				report.user = request.user
				report.save()
				return redirect('forum_post', id=id)
			else:
				post_report_form = PostReportForm()
				return render(request, 'forum_post.html', context)
		elif 'report-comment-submit' in request.POST:  # Handle review report form submission
			comment_report_form = CommentReportForm(request.POST)
			if comment_report_form.is_valid():
				report = comment_report_form.save(commit=False)
				report.reported_comment = get_object_or_404(Comment, pk=request.POST.get('comment_id'))
				report.user = request.user
				report.save()
				return redirect('forum_post', id=id)
			else:
				comment_report_form = CommentReportForm()
				return render(request, 'forum_post.html', context)
		elif 'report-reply-submit' in request.POST:  # Handle review report form submission
			reply_report_form = ReplyReportForm(request.POST)
			if reply_report_form.is_valid():
				report = reply_report_form.save(commit=False)
				report.reported_reply = get_object_or_404(Reply, pk=request.POST.get('reply_id'))
				report.user = request.user
				report.save()
				return redirect('forum_post', id=id)
			else:
				reply_report_form = ReplyReportForm()
				return render(request, 'forum_post.html', context)
		
	
	return render(request, 'forum_post.html',context)

def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        post.dislikes.remove(request.user) # Remove user from dislikes if they liked the post
    return redirect('forum_post', id=post_id)

def dislike_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
    else:
        post.dislikes.add(request.user)
        post.likes.remove(request.user) # Remove user from likes if they disliked the post
    return redirect('forum_post', id=post_id)


def reported_reviews(request):
	reported_reply = ReplyReport.objects.all()
	reported_comment = CommentReport.objects.all()
	reported_post = PostReport.objects.all()
	reported_reviews = ReviewReport.objects.all()  # Retrieve all reported reviews
	return render(request, 'reported_reviews.html', {'reported_reviews': reported_reviews,'reported_post':reported_post,
												  'reported_comment':reported_comment,'reported_reply':reported_reply})

def remove_review(request):
    if request.method == 'POST':
        review_id = request.POST.get('review_id')
        review = Review.objects.filter(id=review_id).first()
        if review:
            review.delete()
    return redirect('reported_reviews')  # Redirect back to the reported_reviews page

def remove_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = Post.objects.filter(id=post_id).first()
        if post:
            post.delete()
    return redirect('reported_reviews')

def remove_comment(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        comment = Comment.objects.filter(id=comment_id).first()
        if comment:
            comment.delete()
    return redirect('reported_reviews')

def remove_reply(request):
    if request.method == 'POST':
        reply_id = request.POST.get('reply_id')
        reply = Reply.objects.filter(id=reply_id).first()
        if reply:
            reply.delete()
    return redirect('reported_reviews')

def user_profile(request):
	user_id = request.user.id
	
	profile, created = UserProfile.objects.get_or_create(user=request.user)
	
	genres_data = AniconnectAniDesc.objects.filter(
    animestatus__user_id=user_id,
    animestatus__status='watched'
	).values_list('genres', flat=True)

	genre_counts = {}
	for genres in genres_data:
		for genre in genres.split(','):
			genre_counts[genre.strip()] = genre_counts.get(genre.strip(), 0) + 1

    # Select top 4 genres and calculate total count for other genres
	sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)
	top_genres = sorted_genres[:4]
	other_count = sum(count for genre, count in sorted_genres[4:])

    # Prepare chart data
	xlab = [genre[0] for genre in top_genres] + ['Other']
	yValues = [genre[1] for genre in top_genres] + [other_count]
	bgColor = ['#ff6384', '#36a2eb', '#ffce56', '#4bc0c0', '#9966ff']
	
	current_user = request.user
	anime_status= AnimeStatus.objects.filter(user=current_user)
	watched=0
	plan_to_watch=0
	dropped=0
	currently_watching=0
	total=0
	for x in anime_status:
		if x.status=="watched":
			watched+=1
		elif x.status=="currently-watching":
			currently_watching+=1
		elif x.status=="dropped":
			dropped+=1
		elif x.status=="plan-to-watch":
			plan_to_watch+=1
		total+=1
	if total>0:
		anime_stat={'watched':watched,
			 'currently-watching':currently_watching,
			 'dropped':dropped,
			 'plan_to_watch':plan_to_watch}
	
		percent_stat={}
		for key,values in anime_stat.items():
			percent_stat[key]= int(((values/total)*100))
	
		diff = 100 - sum(percent_stat.values())
	
		max_key = max(percent_stat, key=percent_stat.get)
		percent_stat[max_key] += diff
	else:
		anime_stat={'watched':watched,
			 'currently-watching':currently_watching,
			 'dropped':dropped,
			 'plan_to_watch':plan_to_watch}
		percent_stat={}
	
	context = {'anime_status':anime_status, 'current_user': current_user,
			'anime_stat':anime_stat,'percent_stat':percent_stat,'genres_data':genres_data,
			'xlab': xlab, 'yValues': yValues, 'bgColor': bgColor,'profile':profile}
	
	return render(request, 'user_profile.html', context)