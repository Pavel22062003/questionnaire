from django.core.management import BaseCommand
from loguru import logger

from user.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(email='admin@root.com', is_staff=True, is_superuser=True)
        user.set_password('1234')
        user.save()
        logger.info(f'created user email - {user.email}, password - {1234}')
