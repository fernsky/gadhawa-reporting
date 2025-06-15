from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a superuser for admin access'

    def handle(self, *args, **options):
        if User.objects.filter(username='admin').exists():
            self.stdout.write(self.style.WARNING('Superuser "admin" already exists'))
            return
        
        user = User.objects.create_superuser(
            username='admin',
            email='admin@lungri.local',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created superuser: {user.username}')
        )
        self.stdout.write(
            self.style.SUCCESS('Login: admin / Password: admin123')
        )
