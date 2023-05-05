from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from decouple import config


class CustomUserManager(BaseUserManager):

    def _create(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        return self._create(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    use_in_migrations = True

    username = None
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=8, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, obj):
        return self.is_staff

    @staticmethod
    def generate_activation_code():
        from django.utils.crypto import get_random_string
        code = get_random_string(8)
        return code 

    def set_activation_code(self):
        code = self.generate_activation_code()
        if CustomUser.objects.filter(activation_code=code).exists():
            self.set_activation_code()
        else:
            self.activation_code = code
            self.save()

    def send_activation_code(self):
        activation_url = f"{config('LINK')}account/activate/{self.activation_code}"
        message = f'''
            You are signed up successfully!
            Activate your account {activation_url}
        '''
        send_mail('Activate your account', message, 'test@gmail.com', [self.email, ])
    
    def password_confirm(self):
        activation_url = f"{config('LINK')}account/forgot_password/{self.activation_code}"
        message = f"""
        Do you want to change password?
        Confirm password changes: {activation_url}
        """
        send_mail(
            "Please confirm new changes", 
            message, "test@gmail.com", [self.email, ]
        )

