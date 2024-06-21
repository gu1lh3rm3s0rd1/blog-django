from django.utils import timezone
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from blog.models import Post


class CommentManager(models.Manager):
    """
    Manager for the Comment model.
    """
    def create_comment(self, post, user, content):
        """
        Create a new comment.
        """
        content_type = ContentType.objects.get_for_model(post.__class__)
        object_id = post.id
        comment = self.create(content_type=content_type,
                              object_id=object_id, user=user, post=post, content=content)
        return comment

    def filter_by_instance(self, instance):
        """
        Filter comments by instance of a model.
        """
        content_type = ContentType.objects.get_for_model(instance.__class__)
        object_id = instance.id
        return self.filter(content_type=content_type, object_id=object_id)


class Comment(models.Model):
    """
    Comment model representing a comment on a blog post.
    """
    # post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments', null=True)
    # post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(default='No comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    objects = CommentManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        """
        String representation of the Comment model.
        """
        return self.content

    def children(self):  # replies
        """
        Get children comments of a comment.
        """
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        """
        Check if a comment is a parent comment.
        """
        if self.parent is None:
            return True
        return False


class Reply(models.Model):
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(default='')
    created_at = models.DateTimeField(default=timezone.now)
