from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic import ListView
from django.core.mail import send_mail

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm


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
    
    # list of comments for this post
    comments = Comment.objects.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            # assign the current post to the comment
            new_comment.post = post
            # save the comment
            new_comment.save()
    else:
        comment_form = CommentForm()


    context = {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'commemt_form': comment_form
    }
    
    return render(request, 'blog/post/detail.html', context)


def post_share(request, post_id):
    # share a post via email
    post = get_object_or_404(Post, id=post_id, 
                             status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            
            subject = f"{cd['name']} recommends you read {post.title}"

            message = f"Read {post.title} at {post_url} \n\n"
            f"{cd['name']}\'s comments: {cd['comments']}"

            send_mail(subject, message, 'testuser013.kenya@gmail.com',
                      [cd['to']])
            sent = True
        
    else:
        form = EmailPostForm()
    
    context = {
        'form': form,
        'sent': sent
    }

    return render(request, 'blog/post/share.html', context)







