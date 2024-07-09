from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

def post_list(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list,1)
    page_number = request.GET.get('page',1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(request,'blog/post/list.html',{'posts':posts})
# class PostListView(ListView):
#     """ Alternative post list view  """
#     model = Post
#     context_object_name = 'posts'
#     paginate_by = 1
#     tmeplate_name = 'blog/post/list.html'

def post_detail(request,id):
    # The first way
    #try:
     #   post = Post.objects.get(id=id)
    #except Post.DoesNotExist:
    #    raise Http404("No Post Found")
    #return render(request,'blog/post/details.html',{'post':post})
    # The second way
    post = get_object_or_404(Post,id=id,status=Post.Status.PUBLISHED)
    return render(request,'blog/post/details.html',{'post':post})

    def post_share(request,post_id):
       # Retrieve post by id
       post = get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
       sent = False
       if request.method == 'Post':
           # form was submitted
           form = EmailPostForm(request.POST)
           if form.is_valid():
               # Form field passed validation
               cd = form.cleaned_data
               post_url = request.build_absolute_url(post.get_absolute_url())
               subject =f"{cd['name']} recommends you read {post.title}"
               message = f"Read{post.title} at {post_urll} \n {cd['name']}\'s comments: {cd['comments']}"
               send_mail(subject,message,'darkomar44@gmail.com',[cd['to']])
               sent = True
               # ... send email
           #else:
            #   form = EmailPostForm()
