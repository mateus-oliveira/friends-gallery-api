from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from .signals import password_reset_token_created

# Register your models here.


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(
            username=username,
            email=email,
            password=password,
            **extra_fields,
        )
        user.save()
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(PermissionsMixin, AbstractBaseUser):
    ROLE_CHOICES = (
        (1, 'married'),
        (2, 'friend'),
    )
    asset = models.ForeignKey(
        'asset.Asset', verbose_name='Profile image',
        on_delete=models.SET_NULL, null=True,
    )
    email = models.EmailField(
        verbose_name='E-mail', max_length=60,
        unique=True, null=False, blank=False,
    )
    username = models.CharField(
        verbose_name='Username', max_length=30,
        unique=True, null=False, blank=False,
    )
    first_name = models.CharField(
        verbose_name='First name', max_length=30, null=False, blank=False,
    )
    last_name = models.CharField(
        verbose_name='Last name', max_length=60, null=False, blank=False,
    )
    role = models.PositiveSmallIntegerField(
        verbose_name='User role',
        choices=ROLE_CHOICES, null=False, blank=False,
    )
    created = models.DateTimeField(
        verbose_name='Created at', auto_now_add=True,
    )
    password = models.CharField(
        verbose_name='Password', max_length=128, null=False, blank=False,
    )

    is_staff = models.BooleanField('Is Staff', default=False)  # django user
    is_active = models.BooleanField('Is Active', default=True)  # django user

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_sha256'):
            self.password = make_password(self.password)

        super(User, self).save(*args, **kwargs)
