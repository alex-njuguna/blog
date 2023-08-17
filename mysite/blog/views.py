from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import ListView

from .models import Post
from .forms import EmailPostForm


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


"""
def post_list(request):
   # display all published post
    object_list = Post.published.all()

    paginator = Paginator(object_list, 3) # 3 posts in each page

    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    context = {
        'page': page,
        'posts': posts
    }

    return render(request, 'blog/post/list.html', context)
"""

def post_detail(request, year, month, day, post):
    """show a specific post"""
    post = get_object_or_404(Post,slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    context = {
        'post': post
    }
    
    return render(request, 'blog/post/detail.html', context)


def post_share(request, post_id):
    # share a post via email
    post = get_object_or_404(Post, id=post_id, 
                             status='published')
    if request.method == 'POST':
        form = EmailPostForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
        
    else:
        form = EmailPostForm()
    
    context = {
        'form': form
    }

    return render(request, 'blog/post/share.html', context)







