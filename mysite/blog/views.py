from django.shortcuts import render, get_object_or_404
from blog.models import Post
from django.http import Http404

def post_list(request):
    posts = Post.objects.all()
    return render(request,'blog/post/list.html',{'posts':posts})

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