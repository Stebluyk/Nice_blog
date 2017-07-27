# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from imagekit.models import ProcessedImageField
from model_utils.managers import InheritanceManager
from model_utils.models import TimeStampedModel
from pilkit.processors import ResizeToFill
from taggit.managers import TaggableManager


class User(AbstractUser):
    avatar = ProcessedImageField(upload_to='avatars', processors=[ResizeToFill(250, 250)], format='JPEG',
                                 options={'quality': 80}, null=True, blank=True)
    description = models.TextField(_('Description'), null=True, blank=True)

    objects = UserManager()

    def get_absolute_url(self):
        return reverse('profile-public', kwargs={'pk': self.id})

    def get_user_posts(self):
        return Post.objects.filter(author=self)

    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        return '/media/avatars/default.jpg'

    def get_messages_opponents(self):
        users = set()
        for m in PrivateMessages.objects.filter(receiver=self):
            users.add(m.sender)
        for m in PrivateMessages.objects.filter(sender=self):
            users.add(m.receiver)
        return list(users)


class Record(TimeStampedModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Author'))

    objects = InheritanceManager()

    class Meta:
        ordering = ['-created']

    def get_comments(self):
        return Comment.objects.filter(record=self)


class Post(Record):
    title = models.CharField(_('Title'), max_length=256)
    image = models.ImageField(_('Post logo'), upload_to='posts/', null=True, blank=True)
    views = models.IntegerField(_('Views'), default=0)
    tags = TaggableManager()
    text = models.TextField()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.id})

    def get_update_url(self):
        return reverse('post-update', kwargs={'pk': self.id})


class Comment(Record):
    record = models.ForeignKey(Record, related_name='parent')
    text = models.TextField(_('Text'))


class PrivateMessages(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sender', verbose_name=_('Sender'))
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='receiver', verbose_name=_('Receiver'))
    text = models.TextField(_('Text message'))
    time_send = models.DateTimeField(_('Time send'), auto_now_add=True)

    class Meta:
        ordering = ['-time_send']
