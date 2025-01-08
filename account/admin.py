from django.contrib import admin

from account.models import Lessons, Homework, Mark


@admin.register(Lessons)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date_of_lesson', 'time_of_lesson')
    list_filter = ('id',)

    def homeworks_list(self, obj):
        return ", ".join([hw.text_task for hw in obj.homeworks.all()])

    homeworks_list.short_description = 'Домашние задания'  # Название колонки в админке

    def students_list(self, obj):
        return ", ".join([st.text_task for st in obj.students.all()])

    homeworks_list.short_description = 'Ученики'  # Название колонки в админке


@admin.register(Homework)
class UserAdmin(admin.ModelAdmin):
    list_display = ('homework_task', 'mark')
    list_filter = ('id',)

@admin.register(Mark)
class UserAdmin(admin.ModelAdmin):
    list_display = ('homework_mark', 'comment', 'homework_submission')
    list_filter = ('id',)
