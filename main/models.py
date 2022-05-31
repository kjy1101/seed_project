from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, name, organization, login_id, email, password, **kwargs):
        if not email:
            raise ValueError(_('Users must have an email address'))

        user = self.model(
            name=name,
            organization=organization,
            login_id=login_id,
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name=None, organization=None, login_id=None, email=None, password=None, **extra_fields):
        superuser = self.create_user(
            login_id=login_id,
            email=email,
            password=password,
            organization=organization,
            name=name
        )
        superuser.name = "관리자"
        superuser.organization = "관리자"
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.save(using=self._db)
        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    login_id = models.CharField(max_length=30, unique=True, null=False, blank=False)
    email = models.EmailField(max_length=30, unique=True, null=False, blank=False)
    name = models.CharField(max_length=30, null=True, blank=True)
    organization = models.CharField(max_length=30, null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'login_id'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'user'

