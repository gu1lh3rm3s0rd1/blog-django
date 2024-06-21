from django import forms
from .models import Post
from comments.models import Comment
from pagedown.widgets import PagedownWidget


class PostForm(forms.ModelForm):
    """
    Form for creating and updating Post instances.
    """
    title = forms.CharField(label='Título', widget=forms.TextInput(
        attrs={'class': 'create-title'}))
    description = forms.CharField(label='Descrição', widget=forms.TextInput(
        attrs={'class': 'create-description'}))
    content = forms.CharField(label='Conteúdo', widget=PagedownWidget(
        attrs={'class': 'create-content'}))

    class Meta:
        model = Post
        fields = ['title', 'description', 'content']
