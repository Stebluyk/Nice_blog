"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from blog.views import ProfileView, PostCreateView, PostListView, PostDetailView, UserPostListView, \
    CommentListView, MessagesListView, MessagesUserView, UserView, PostUpdateView

post_urls = [
    url(r'^create/$', PostCreateView.as_view(), name='post-create'),
    url(r'^update/(?P<pk>[-\w]+)/$', PostUpdateView.as_view(), name='post-update'),
    url(r'^my/$', UserPostListView.as_view(), name='post-list-user'),
    url(r'^comments/$', CommentListView.as_view(), name='comment-list-user'),
    url(r'^(?P<pk>[-\w]+)/$', PostDetailView.as_view(), name='post-detail'),
]

messages_urls = [
    url(r'^$', MessagesListView.as_view(), name='message_list'),
    url(r'^(?P<user>[-\w]+)/$', MessagesUserView.as_view(), name='message'),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', PostListView.as_view(), name='post-list'),
    url(r'^accounts/profile/$', ProfileView.as_view(), name='profile'),
    url(r'^user/(?P<pk>[-\w]+)/$', UserView.as_view(), name='profile-public'),

    url(r'^posts/', include(post_urls)),
    url(r'^messages/', include(messages_urls)),
    url(r'^summernote/', include('django_summernote.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
