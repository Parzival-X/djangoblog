from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.utils import timezone
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from myblog.models import Post, Category
from myblog.forms import MyPostForm
from myblog.serializers import UserSerializer, GroupSerializer, PostSerializer, CategorySerializer


def stub_view(request, *args, **kwargs):
    body = "Stub View\n\n"
    if args:
        body += "Args:\n"
        body += "\n".join(["\t%s" % a for a in args])
    if kwargs:
        body += "Kwargs:\n"
        body += "\n".join(["\t%s: %s" % i for i in kwargs.items()])
    return HttpResponse(body, content_type="text/plain")


def list_view(request):
    published = Post.objects.exclude(published_date__exact=None)
    posts = published.order_by('-published_date')
    context = {'posts': posts}
    return render(request, 'list.html', context)


def detail_view(request, post_id):
    published = Post.objects.exclude(published_date__exact=None)
    try:
        post = published.get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404
    context = {'post': post}
    return render(request, 'detail.html', context)


# View for Post Model Views
def post_create_view(request):

    if request.method == "POST":
        form = MyPostForm(request.POST)

        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.published_date = timezone.now()
            model_instance.author = request.user
            model_instance.save()
            return redirect('/')
    else:
        form = MyPostForm()
        context = {'form': form}
        return render(request, "post_create_view.html", context)


# Views for REST frameworks
class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for all Users ordered by active accounts.
    """
    queryset = User.objects.all().order_by('-is_active')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    ViewSet for all Groups ordered by name.
    """
    queryset = Group.objects.all().order_by('-name')
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for all Posts ordered by published date.
    """
    queryset = Post.objects.all().order_by('-published_date')
    serializer_class = PostSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for all Categories ordered by name.
    """
    queryset = Category.objects.all().order_by('-name')
    serializer_class = CategorySerializer
