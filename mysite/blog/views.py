from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST

# def post_list(request):
#     post_list = Post.objects.all()
#     paginator = Paginator(post_list,2)
#     page_number = request.GET.get('page',1)
#     try:
#         posts = paginator.page(page_number)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     return render(request,'blog/post/list.html',{'posts':posts})
class PostListView(ListView):
#     """ Alternative post list view  """
     model = Post
     context_object_name = 'posts'
     paginate_by = 2
     template_name = 'blog/post/list.html'

def post_detail(request,id):
    # The first way
    #try:
     #   post = Post.objects.get(id=id)
    #except Post.DoesNotExist:
    #    raise Http404("No Post Found")
    #return render(request,'blog/post/details.html',{'post':post})
    # The second way
    post = get_object_or_404(Post,id=id,status=Post.Status.PUBLISHED)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()
    return render(request,'blog/post/details.html',{'post':post,'comments':comments,'form':form})

def post_share(request,post_id):
    # Retrieve post by id
    post = get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        # form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form field passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject =f"{cd['name']} recommends you read {post.title}"
            message = f"Read{post.title} at {post_url} \n {cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject,message,'darkomar44@gmail.com',[cd['to']])
            sent = True
            # ... send email 
    else:
        form = EmailPostForm()
    return render(request,'blog/post/share.html',{'post':post,'form':form,'sent':sent})
@require_POST 
def post_comment(request,post_id):
    post = get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    return render(request,'blog/post/comment.html',{'post':post,'form':form,'comment':comment})


