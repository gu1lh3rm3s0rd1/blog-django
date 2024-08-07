from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from django.utils.safestring import mark_safe
import markdown2
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify


class Post(models.Model):
    """
    Post model representing a blog post.
    """
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    content = MarkdownxField()
    cover_image = models.ImageField(upload_to='cover_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    

    def save(self, *args, **kwargs):
            if not self.slug:
                self.slug = slugify(self.title)
            super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation of the Post model.
        """
        return self.title

    def get_markdown(self):
        """
        Converts the markdown content to HTML.
        """
        content = markdown2.markdown(self.content)
        return mark_safe(content)

    def num_comments(self):
        """
        Returns the number of comments on the post.
        """
        return self.comments.count()

    @property
    def comments(self):
        """
        Returns the comments on the post.
        """
        return self.comments_set.all()

    @property
    def get_content_type(self):
        """
        Returns the comments on the post.
        """
        content_type = ContentType.objects.get_for_model(self.__class__)

        return content_type
