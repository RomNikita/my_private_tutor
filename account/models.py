from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from slugify import slugify
from users.models import NULLABLE, User


class HomeworkSubmission(models.Model):
    homework = models.ForeignKey('Homework', on_delete=models.CASCADE, verbose_name='задание для дз')
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ученик')
    submission_date = models.DateField(auto_now_add=True, verbose_name='дата сдачи')
    submission_time = models.TimeField(auto_now_add=True, verbose_name='время сдачи')
    file = models.FileField(upload_to='homework_submissions', verbose_name='файл сдачи', **NULLABLE)
    is_completed = models.BooleanField(default=False, verbose_name='выполнено')

    class Meta:
        verbose_name = 'сдача дз'
        verbose_name_plural = 'сдачи дз'


class Mark(models.Model):
    homework_mark = models.IntegerField(verbose_name='оценка к дз',
                                        validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)
    homework_submission = models.OneToOneField('HomeworkSubmission', on_delete=models.CASCADE, verbose_name='сдача дз')

    class Meta:
        verbose_name = 'оценка'
        verbose_name_plural = 'оценки'


class Homework(models.Model):
    homework_task = models.TextField(verbose_name='задание для дз')
    mark = models.ForeignKey(Mark, on_delete=models.CASCADE, verbose_name='оценка', **NULLABLE)
    materials = models.FileField(upload_to='homeworks')
    students = models.ManyToManyField(User, verbose_name='ученики', blank=True)

    class Meta:
        verbose_name = 'домашнее задание'
        verbose_name_plural = 'домашние задания'


class Lessons(models.Model):
    title = models.CharField(max_length=250, verbose_name='название', default='')
    date_of_lesson = models.DateField(verbose_name='дата урока')
    time_of_lesson = models.TimeField(verbose_name='время урока')
    homeworks = models.ManyToManyField(Homework, verbose_name='Д/З урока', blank=True)
    students = models.ManyToManyField(User, verbose_name='ученики', related_name='lessons', blank=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
