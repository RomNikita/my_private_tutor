from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DetailView

from account.forms import LessonCreateForm, HomeworkCreateForm
from account.models import Homework, Lessons
from users.models import User


class MainPageView(TemplateView):
    template_name = 'account_main_page.html'


class LessonsListView(LoginRequiredMixin, ListView):
    model = Lessons
    template_name = 'account_main_page.html'
    context_object_name = 'lessons'

    def get_queryset(self):

        student = self.request.user
        if student.is_staff:
            return Lessons.objects.all().order_by('date_of_lesson')
        return Lessons.objects.filter(students=student).order_by('date_of_lesson')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lesson_dates'] = [
            lesson.date_of_lesson.strftime('%Y-%m-%d') for lesson in self.get_queryset()
        ]
        return context


class LessonsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Lessons
    form_class = LessonCreateForm
    template_name = 'lessons_form.html'
    success_url = reverse_lazy('account:account_main_page')
    permission_required = 'account.create_lesson'


class HomeworkListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Homework
    template_name = 'homework_list.html'
    context_object_name = 'homeworks'
    permission_required = 'account.view_homework'

    def get_queryset(self):
        student = self.request.user
        if student.is_staff:
            return Homework.objects.all()
        return Homework.objects.filter(students=student)

    def get_context_data(self, *, object_list=None, **kwargs):
        pass


class LessonsDetailView(LoginRequiredMixin,  DetailView):
    model = Lessons
    template_name = 'lessons_id.html'
    context_object_name = 'lesson'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class HomeworkCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Homework
    form_class = HomeworkCreateForm
    template_name = 'homework_create.html'
    permission_required = 'account.create_homework'

    def form_valid(self, form):
        # Получаем урок по slug
        lesson_slug = self.kwargs.get('lesson_slug')
        lesson = get_object_or_404(Lessons, slug=lesson_slug)

        # Сохраняем домашнее задание без привязки к урокам
        homework = form.save()

        # Добавляем домашнее задание к уроку
        lesson.homeworks.add(homework)

        messages.success(self.request, 'Домашнее задание успешно создано!')
        return super().form_valid(form)

    def get_success_url(self):
        lesson_slug = self.kwargs.get('lesson_slug')
        return reverse_lazy('account:lessons_detail', kwargs={'slug': lesson_slug})


class TeacherLessonsView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'teacher_lessons.html'  # Новый шаблон для учителей
    context_object_name = 'students'

    def get_queryset(self):
        return User.objects.filter(groups__name='Ученики')


class StudentLessonsView(LoginRequiredMixin, ListView):
    model = Lessons
    template_name = 'for_teacher_st_lessons.html'
    context_object_name = 'lessons'

    def get_queryset(self):
        student = User.objects.get(id=self.kwargs['student_id'])  # Получаем ученика по ID
        return Lessons.objects.filter(students=student).order_by('date_of_lesson')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = get_object_or_404(User, id=self.kwargs['student_id'])
        context['student'] = student  # Добавляем объект student в контекст
        return context




