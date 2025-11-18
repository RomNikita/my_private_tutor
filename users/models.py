from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

NULLABLE = {'blank': True, 'null': True}


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, email=None, password=None, **extra_fields):
        if not phone:
            raise ValueError('Phone number is required')

        email = self.normalize_email(email) if email else None
        user = self.model(phone=phone, email=email, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not password:
            raise ValueError('Superuser must have a password')

        return self.create_user(phone, email, password, **extra_fields)


class User(AbstractUser):
    # Удаляем стандартное поле username
    username = None

    # Задаём свои поля
    email = models.EmailField(max_length=150, verbose_name='электронная почта', **NULLABLE)
    phone = models.CharField(max_length=50, unique=True, verbose_name='номер телефона')
    name = models.CharField(max_length=100, verbose_name='имя')
    surname = models.CharField(max_length=100, verbose_name='фамилия')
    date_of_birth = models.DateField(verbose_name='дата рождения', **NULLABLE)

    avatar = models.ImageField(upload_to='user', verbose_name='аватар', **NULLABLE)

    # Настройки авторизации
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.name} {self.surname} (тел: {self.phone})'

    def clean(self):
        super().clean()
        if self.email:
            existing_user = User.objects.filter(email=self.email).exclude(pk=self.pk).first()
            if existing_user:
                raise ValidationError({'email': 'Email must be unique'})


# Добавление пользователя в группу "Ученики" после создания
@receiver(post_save, sender=User)
def add_user_to_students_group(sender, instance, created, **kwargs):
    if created:
        group, _ = Group.objects.get_or_create(name='Ученики')
        instance.groups.add(group)