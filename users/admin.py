from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'phone', 'email', 'date_of_birthday', 'display_groups')
    list_filter = ('id',)

    def display_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])