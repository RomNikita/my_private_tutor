from django.urls import path

from account.views import MainPageView, LessonsListView, HomeworkListView, LessonsCreateView, LessonsDetailView, \
    HomeworkCreateView

app_name = 'account'

urlpatterns = [
    path('', LessonsListView.as_view(), name='account_main_page'),
    path('homework/', HomeworkListView.as_view(), name='homework_list'),
    path('create/', LessonsCreateView.as_view(), name='lessons_create'),
    path('lesson/<slug:slug>/', LessonsDetailView.as_view(), name='lessons_detail'),
    path('homework/create/<slug:lesson_slug>/', HomeworkCreateView.as_view(), name='homework_create')
]