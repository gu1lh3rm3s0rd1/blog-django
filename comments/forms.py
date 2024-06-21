from django import forms
from .models import Comment
from .models import Reply


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['post', 'user', 'content_type', 'object_id', 'parent', 'text']
        labels = {
            'content': '',
        }
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Deixe um comentário aqui',
                    'id': 'floatingTextarea',
                    'style': 'height: 100px',
                    'width': '100%',
                    'resize': 'none'
                }
            )
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
