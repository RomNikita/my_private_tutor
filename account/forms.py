from django import forms

from account.models import Lessons, Homework


class LessonCreateForm(forms.ModelForm):
    class Meta:
        model = Lessons
        fields = ['title', 'date_of_lesson', 'time_of_lesson', 'students']

    date_of_lesson = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата урока'
    )

    time_of_lesson = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label='Время урока'
    )


class HomeworkCreateForm(forms.ModelForm):
    materials = forms.FileField(required=False)  # Поле для загрузки одного файла

    class Meta:
        model = Homework
        fields = ['homework_task', 'materials']
        widgets = {
            'homework_task': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Введите задание здесь...'}),
        }
