from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import Group

NULLABLE = {'blank': True, 'null': True}


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, email, password=None, **extra_fields):
        if not email and not phone:
            raise ValueError('The email or phone must be set')
        email = self.normalize_email(email) if email else None
        user = self.model(phone=phone, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone, email, password, **extra_fields)


class User(AbstractUser):
    username = None

    email = models.EmailField(max_length=150, verbose_name='электронная почта', **NULLABLE)
    password = models.CharField(max_length=100, verbose_name='пароль')
    phone = models.CharField(max_length=50, unique=True, verbose_name='номер телефона')
    avatar = models.ImageField(upload_to='user', verbose_name='аватар')
    name = models.CharField(max_length=100, verbose_name='имя')
    surname = models.CharField(max_length=100, verbose_name='фамилия')
    date_of_birthday = models.DateField(verbose_name='дата рождения')
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.name} {self.surname}'

    def clean(self):
        super().clean()
        if self.email:
            existing_user = User.objects.filter(email=self.email).exclude(pk=self.pk).first()
            if existing_user:
                raise ValidationError({'email': 'Email must be unique'})

    def save(self, *args, **kwargs):
        # Сохраняем пользователя в базе данных, чтобы получить его id
        if self._state.adding:
            super().save(*args, **kwargs)  # Сначала сохраняем пользователя, чтобы получить ID

            # После того как пользователь сохранен, добавляем его в группу "Ученики"
            students_group, created = Group.objects.get_or_create(name='Ученики')
            self.groups.add(students_group)

        # Валидация и повторное сохранение пользователя
        self.clean()
        super().save(*args, **kwargs)
