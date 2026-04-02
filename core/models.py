from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class Institution(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_learning_institution = models.BooleanField(default=False)
    is_care_institution = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Badge(models.Model):
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.description or f"Badge {self.id}"


class UseCase(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class User(AbstractUser):
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    function = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    ai_knowledge_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        blank=True,
        null=True
    )
    points = models.IntegerField(default=0)
    rank = models.CharField(max_length=255, blank=True, null=True)
    is_admin = models.BooleanField(default=False)

    institution = models.ForeignKey(
        Institution,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users"
    )

    badges = models.ManyToManyField(
        Badge,
        blank=True,
        related_name="users"
    )

    def __str__(self):
        return self.username


class Post(models.Model):
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    short_description = models.CharField(max_length=500)
    long_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image_path = models.CharField(max_length=500, blank=True, null=True)
    target_audience = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    is_validated = models.BooleanField(default=False)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    use_case = models.ForeignKey(
        UseCase,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts"
    )

    institution = models.ForeignKey(
        Institution,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts"
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    comment_text = models.TextField()

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    def __str__(self):
        return f"Comment {self.id}"


class Like(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "post"], name="unique_user_post_like")
        ]

    def __str__(self):
        return f"Like {self.id}"


class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    def __str__(self):
        return self.title 
