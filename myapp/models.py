from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.auth.models import AbstractUser, Group


def validate_image(image):
    file_size = image.file.size
    limit_mb = 2
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError("Max size of file is %s MB" % limit_mb)


class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True,
                                        validators=[validate_image])
    bio = models.TextField(null=True, blank=True)
    groups = models.ManyToManyField(Group, blank=True, related_name='myapp_users')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='myapp_users')


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def clean(self):
        if ' ' in self.name:
            raise ValidationError("Tag names cannot contain spaces.")


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    likes = models.ManyToManyField(User, through='Like', related_name='liked_posts')

    def clean(self):
        if not self.content:
            raise ValidationError("Posts cannot be blank.")


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Example validation rule: Comments cannot be too long
        if len(self.content) > 500:
            raise ValidationError("Comments cannot be longer than 500 characters.")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='following')


class Feed(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    posts = models.ManyToManyField(Post, related_name='feed_posts')


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class DirectMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
