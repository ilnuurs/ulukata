from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if email is None:
            raise ValueError(_("email must be set"))
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    username = None 
    email = models.EmailField(verbose_name="почта", unique=True, blank=False, null=False)
    phone = PhoneNumberField(verbose_name="телефон", blank=True, null=True) 
    avatar = ResizedImageField(size=[500, 500], crop=['middle', 'center'], upload_to='avatars/', blank=True, null=True, verbose_name="аватар", quality=90)
    date_of_birth = models.DateField(verbose_name="дата рождения", blank=True, null=True)
    gender = models.CharField(max_length=10, verbose_name='пол', choices=[("man", 'мужчина'), ('woman', 'женщина')], blank=True, null=True)
    
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email 
    
    
class OTPcode(models.Model):
    class Meta:
        verbose_name = 'OTP code'
        verbose_name_plural = "OTP code"
        
    email = models.EmailField()
    code = models.CharField(max_length=6)
    create_at = models.DateTimeField(auto_now_add=True)
    expire_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expire_at:
            self.expire_at = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs) 
    
    def is_expired(self):
        return timezone.now() > self.expire_at
    
    def __str__(self):
        return f'{self.email} - {self.code}'