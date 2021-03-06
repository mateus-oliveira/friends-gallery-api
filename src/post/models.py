from django.db import models

# Create your models here.


class Post(models.Model):
    STATUS = [
        (1, 'pending'),
        (2, 'approved'),
        (3, 'disapproved'),
    ]

    asset = models.ForeignKey(
        'asset.Asset', verbose_name='Image',
        null=False, on_delete=models.PROTECT,
    )
    user = models.ForeignKey(
        'authentication.User', verbose_name='User',
        null=False, on_delete=models.PROTECT, related_name='post_owner',
    )
    likes = models.ManyToManyField(
        'authentication.User', related_name='post_followers',
    )
    caption = models.CharField(
        verbose_name='Caption', max_length=300, null=False, blank=False,
    )
    status = models.PositiveSmallIntegerField(choices=STATUS, default=1)
    created = models.DateTimeField(
        verbose_name='Created at', auto_now_add=True,
    )

    def __str__(self) -> str:
        return f'Post {self.id}: "{self.caption}" - {self.user}'


class Comment(models.Model):
    post = models.ForeignKey(
        'post.Post', verbose_name='Post',
        null=False, on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        'authentication.User', verbose_name='User',
        null=False, on_delete=models.CASCADE,
    )
    text = models.CharField(
        verbose_name='Comment text', max_length=200, null=False, blank=False,
    )
    created = models.DateTimeField(
        verbose_name='Created at', auto_now_add=True,
    )

    def __str__(self) -> str:
        return f'Comment {self.id} in Post {self.post.id}: "{self.text}" - {self.user}'
