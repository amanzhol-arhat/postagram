from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.db import models

from core.abstract import AbstractManager, AbstractModel


def user_directory_path(instance, _filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "user_{0}/{1}".format(instance.public_id, _filename)


class UserManager(BaseUserManager, AbstractManager):
    def create_user(self, username, email, password=None, **kwargs):
        if username is None:
            raise TypeError("Users must have a username")
        if email is None:
            raise TypeError("Users must have a email")
        if password is None:
            raise TypeError("Users must have a password")

        user = self.model(
            username=username, email=self.normalize_email(email), **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **kwargs):
        if username is None:
            raise TypeError("Superusers must have a username")
        if email is None:
            raise TypeError("Superusers must have a email")
        if password is None:
            raise TypeError("Superusers must have a password")

        user = self.create_user(username, email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    bio = models.CharField(max_length=300, null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to=user_directory_path)
    avatar_seed = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text="DiceBear seed для стиля 'dylan'",
    )

    posts_liked = models.ManyToManyField("core_post.Post", related_name="liked_by")
    comments_liked = models.ManyToManyField(
        "core_comment.Comment", related_name="commented_by"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def like_post(self, post):
        """Like `post` if it hasn't been done yet"""
        return self.posts_liked.add(post)

    def remove_like_post(self, post):
        """Remove a like from a `post`"""
        return self.posts_liked.remove(post)

    def has_liked_post(self, post):
        """Return True if the user has liked a `post`; else False"""
        return self.posts_liked.filter(pk=post.pk).exists()

    def like_comment(self, comment):
        """Like `comment` if it hasn't been done yet"""
        return self.comments_liked.add(comment)

    def remove_like_comment(self, comment):
        """Remove a like from a `comment`"""
        return self.comments_liked.remove(comment)

    def has_liked_comment(self, comment):
        """Return True if the user has liked a `comment`; else False"""
        return self.comments_liked.filter(pk=comment.pk).exists()


class UserFollow(models.Model):
    user = models.ForeignKey(
        "core_user.User",
        on_delete=models.CASCADE,
        related_name="following",
        help_text="Who is subscribing",
    )
    followed = models.ForeignKey(
        "core_user.User",
        related_name="followers",
        on_delete=models.CASCADE,
        help_text="Who is being subscribed to",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "followed")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "followed"]),
            models.Index(fields=["followed"]),
        ]

    def __str__(self):
        return f"{self.user.username} follows {self.followed.username}"

    def clean(self):
        if self.user == self.followed:
            raise ValidationError("You cannot follow yourself.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
