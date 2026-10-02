from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django_resized import ResizedImageField


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Электронная почта должна быть указана")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(**{self.model.USERNAME_FIELD: email})


class User(AbstractUser):
    # Возвращаем username в базу, чтобы админка не падала, но делаем его не обязательным
    email = models.EmailField(verbose_name="почта", unique=True, blank=False, null=False)
    phone = PhoneNumberField(verbose_name="телефон", blank=True, null=True) 
    avatar = ResizedImageField(size=[500, 500], crop=['middle', 'center'], upload_to='avatars/', blank=True, null=True, verbose_name="аватар", quality=90)
    date_of_birth = models.DateField(verbose_name="дата рождения", blank=True, null=True)
    gender = models.CharField(max_length=10, verbose_name='пол', choices=[("man", 'мужчина'), ('woman', 'женщина')], blank=True, null=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return self.email


class OTPcode(models.Model):
    email = models.EmailField(verbose_name="почта")
    code = models.CharField(max_length=6, verbose_name="код")
    expire_at = models.DateTimeField(verbose_name="время истечения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="время создания")

    @property
    def is_expired(self):
        return timezone.now() > self.expire_at

    class Meta:
        verbose_name = "OTP код"
        verbose_name_plural = "OTP коды"

    def __str__(self):
        return f"{self.email} - {self.code}"