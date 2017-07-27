from datetimewidget.widgets import DateWidget
from django import forms
from django_summernote.widgets import SummernoteInplaceWidget
from taggit.models import Tag

from blog.models import Post, Comment, PrivateMessages


def tags_choices():
    return [('', ' ')] + [(t.name, t.name) for t in Tag.objects.all()]


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'tags', 'text']
        widgets = dict(
            text=SummernoteInplaceWidget(attrs={'width': '100%', 'height': '500px'})
        )


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = dict(
            text=forms.Textarea(attrs={'rows': '4'})
        )


class PostFiltersForm(forms.Form):
    tag = forms.ChoiceField(choices=tags_choices, required=False)
    date_from = forms.DateField(required=False,
                                widget=DateWidget(usel10n=True, bootstrap_version=3, options={'format': 'yyyy-mm-dd'}))
    date_to = forms.DateField(required=False,
                              widget=DateWidget(usel10n=True, bootstrap_version=3, options={'format': 'yyyy-mm-dd'}),)


class MessageCreateForm(forms.ModelForm):
    class Meta:
        model = PrivateMessages
        fields = ['text']
        widgets = dict(
            text=forms.Textarea(attrs={'rows': '5'})
        )
