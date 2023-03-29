
from django.shortcuts import render
from .models import *
from django.views.generic import DetailView, ListView
from  django.core.paginator import Paginator
from django.db.models import F
from .forms import NewComment, LoginForm
from django.shortcuts import redirect
from django.http import HttpResponseNotFound ,JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    posts = Post.objects.order_by('-created_at')[1:]
    last_post =Post.objects.order_by('-created_at')[0]
    print(last_post)
    paginator = Paginator(posts, 6)
    page_obj = paginator.page(request.GET.get('page', 1))
    
    
    return render(request, 'blog_app/index.html',{'page_obj': page_obj, 'last_post': last_post})

  
    
def separate_category(request, slug):
    category = Category.objects.get(slug=slug)
    posts = Post.objects.filter(category__title = category.title).order_by('-created_at')[1:]
    paginator = Paginator(posts, 4)
    page_obj = paginator.page(request.GET.get('page', 1))
    if len(posts) > 0:
        last_post =Post.objects.filter(category__title = category.title).order_by('-created_at')[0]
        return render(request, 'blog_app/index.html',{'category': category, 'page_obj': page_obj, 'last_post':last_post, 'info':category.title})
    else:
        return render(request, 'blog_app/index.html',{'category': category, 'page_obj': page_obj, 'info': f'category {category} is empty'})


class ThePost(DetailView):
    model = Post
    slug_url_kwarg = 'slugi'


    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
       
        self.object.views =F('views') + 1 
        self.object.save()
        self.object.refresh_from_db()
        page = self.request.GET.get('page', 1)
        context['page'] = page
        return context


class ThePostsByTag(ListView):
    template_name ='blog_app/index.html'
    paginate_by = 8

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if len(self.get_queryset()) == 0:
            context['info'] = f'There is no posts related to {self.kwargs["slug"]} tag'
        else:
            context['info'] = self.kwargs["slug"]
        return context

class SearchedPosts(ListView):
    template_name = 'blog_app/index.html'
    paginate_by = 2
    model = Post

    def get_queryset(self):
        return Post.objects.filter(title__icontains= self.request.GET.get('looking_for'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['looking_for'] = f"looking_for={self.request.GET.get('looking_for')}&"
        return context

def add_comment(request):
    if request.method == 'POST':
        form = NewComment(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.save()
    else:
        return HttpResponseNotFound("Page not found")
    return redirect(request.META.get('HTTP_REFERER'))

def register(request):
    if request.method == 'POST':
        register_form = UserCreationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, 'You are succesfull registerered')
            return redirect('login')
        else:
            messages.error(request, 'Registration form error')
    else:
        register_form = UserCreationForm()
    return render(request, 'blog_app/register.html', {'register_form':register_form})


def log_in(request):
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('home')
    else:
        login_form =  LoginForm()
    return render(request, 'blog_app/login.html',{'login_form':login_form})    

def log_out(request):
    logout(request)
    return redirect('home')

@csrf_exempt
def like(request):
    post_data = json.loads(request.body.decode('utf-8'))
    comment = Comment.objects.get(pk=post_data.get('commentId'))
    if request.user in comment.liked.all():
        comment.liked.remove(request.user)
        is_liked = ''
    else:
        comment.liked.add(request.user)
        is_liked = 'true'
    likes = len(comment.liked.all())
    
    return JsonResponse({'likes':likes, 'is_liked':is_liked})

