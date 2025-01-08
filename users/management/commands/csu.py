from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            phone='+79991112231',
            name='Тимофей',
            surname='',
            is_staff=True,
            is_superuser=True,
            is_active=True,
            date_of_birthday='2022-02-22'
        )
        user.set_password('12345qwe')
        user.save()
