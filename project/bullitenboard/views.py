from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView,DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from .forms import PostForm, UserResponseForm
from .models import Post, UserResponse
from .filters import PostFilter
class PostList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 2

    def __str__(self):
        return


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class UserResponseList(ListView):
    model = UserResponse
    ordering = '-response_time'
    template_name = 'responses.html'
    context_object_name = 'responses'
    paginate_by = 2

class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post_detail'


class PostCreate(PermissionRequiredMixin,  CreateView):
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    permission_required = ('bullitenboard.post_create')

class PostEdit(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post')
    permission_required = ('bullitenboard.post_edit')

class ResponseCreate(PermissionRequiredMixin, CreateView):
    raise_exception = True
    form_class = UserResponseForm
    model = UserResponse
    template_name = 'response_create.html'
    success_url = reverse_lazy('posts')