from django.urls import path

from account.views import MainPageView, LessonsListView, HomeworkListView, LessonsCreateView, LessonsDetailView, \
    HomeworkCreateView, TeacherLessonsView, StudentLessonsView

app_name = 'account'

urlpatterns = [
    path('', LessonsListView.as_view(), name='account_main_page'),
    path('homework/', HomeworkListView.as_view(), name='homework_list'),
    path('create/', LessonsCreateView.as_view(), name='lessons_create'),
    path('lesson/<slug:slug>/', LessonsDetailView.as_view(), name='lessons_detail'),
    path('homework/create/<slug:lesson_slug>/', HomeworkCreateView.as_view(), name='homework_create'),
    path('teacher/', TeacherLessonsView.as_view(), name='teacher_lessons'),
    path('teacher/student_lessons/<int:student_id>/', StudentLessonsView.as_view(), name='student_lessons'),
]