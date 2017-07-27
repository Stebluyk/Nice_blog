# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import UpdateView, CreateView, ListView, DetailView
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import FormMixin, ModelFormMixin

from blog.forms import PostCreateForm, CommentCreateForm, PostFiltersForm, MessageCreateForm
from blog.models import User, Post, Comment, PrivateMessages
from blog.utils import CustomPaginatorMixin


class ProfileView(UpdateView):

    title = _('Profile')
    model = User
    fields = ['first_name', 'last_name', 'email', 'avatar', 'description']
    template_name = 'profile.html'
    success_url = '/profile/'

    def get_object(self, queryset=None):
        return self.request.user


class UserView(DetailView):

    model = User
    template_name = 'profile_public.html'

    @property
    def title(self):
        return 'Profile: {}'.format(self.get_object())

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(self.model, id=pk)


class PostCreateView(CreateView):

    title = _('Create post')
    model = Post
    form_class = PostCreateForm
    template_name = 'post_create.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)


class PostUpdateView(UpdateView):

    title = _('Update post')
    model = Post
    form_class = PostCreateForm
    template_name = 'post_create.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostUpdateView, self).form_valid(form)


class PostListView(CustomPaginatorMixin, FormMixin, ListView):

    title = _('Post list')
    model = Post
    template_name = 'post_list.html'
    paginate_by = 5
    form_class = PostFiltersForm

    def get_queryset(self):
        params = dict()
        tag = self.request.GET.get('tag')
        if tag:
            params['tags__name__iexact'] = tag
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        if date_from:
            params['created__gte'] = date_from
        if date_to:
            params['created__lte'] = date_to
        q = super(PostListView, self).get_queryset()
        return q.filter(**params)

    def get_initial(self):
        kwargs = super(PostListView, self).get_initial()
        kwargs.update(self.request.GET.dict())
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        # context['form'] = self.f
        return context


class UserPostListView(PostListView):

    title = _('User post list')

    def get_queryset(self):
        q = super(UserPostListView, self).get_queryset()
        return q.filter(author=self.request.user)


class PostDetailView(CreateView):

    model = Comment
    template_name = 'post_detail.html'
    form_class = CommentCreateForm
    object = None

    @property
    def title(self):
        return self.get_post()

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse('post-detail', kwargs={'pk': pk})

    def get_post(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Post, id=pk)

    def get(self, request, *args, **kwargs):
        post = self.get_post()
        post.views += 1
        post.save()
        context = self.get_context_data(object=post)
        return self.render_to_response(context)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.record = self.get_post()
        return super(PostDetailView, self).form_valid(form)


class CommentListView(CustomPaginatorMixin, ListView):

    title = _('User comments list')
    model = Comment
    template_name = 'comment_list.html'
    paginate_by = 20

    def get_queryset(self):
        q = super(CommentListView, self).get_queryset()
        return q.filter(author=self.request.user)


class MessagesListView(CustomPaginatorMixin, ListView):

    title = _('Private messages')
    template_name = 'messages_list.html'
    paginate_by = 20

    def get_queryset(self):
        return self.request.user.get_messages_opponents()


class MessagesUserView(CustomPaginatorMixin, ModelFormMixin, ListView):

    title = _('Private messages')  # TODO: make func
    model = PrivateMessages
    template_name = 'messages.html'
    paginate_by = 10
    form_class = MessageCreateForm
    object = None

    def get_success_url(self):
        pk = self.kwargs.get('user')
        return reverse('message', kwargs={'user': pk})

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.receiver_id = self.kwargs.get('user')
        return super(MessagesUserView, self).form_valid(form)

    def get_queryset(self):
        sender = get_object_or_404(User, id=self.kwargs.get('user'))
        users = [sender, self.request.user]
        q = super(MessagesUserView, self).get_queryset()
        return q.filter(sender__in=users, receiver__in=users)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
