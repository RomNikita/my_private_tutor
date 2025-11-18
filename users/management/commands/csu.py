from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            phone='+79991112222',
            defaults={
                'name':'reborn',
                'surname':'',
                'is_staff':True,
                'is_superuser':True,
                'is_active':True,
                'date_of_birthday':'2022-02-23',
        }
        )
        if created:
            user.set_password('12345qwe123')
            user.save()
            print('creating superuser')