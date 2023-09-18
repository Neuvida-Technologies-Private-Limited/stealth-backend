from django.core.management.base import BaseCommand
from apps.access.models import User as USER

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not USER.objects.filter(is_superuser=True).exists():
            USER.objects.create_superuser(
                username="admin", email="admin@example.com", password="admin"
            )
            self.stdout.write(self.style.SUCCESS("Admin user has created"))
        else:
            self.stdout.write(self.style.SUCCESS("Admin user already exists"))
