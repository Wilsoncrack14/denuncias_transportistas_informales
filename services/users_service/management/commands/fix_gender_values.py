from django.core.management.base import BaseCommand
from users_service.models import User

class Command(BaseCommand):
    help = 'Corrige los valores de gender de M/F/O a male/female'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Corrigiendo valores de gender...'))
        
        gender_mapping = {
            'M': 'male',
            'F': 'female',
            'O': None, 
        }
        
        updated_count = 0
        
        for old_value, new_value in gender_mapping.items():
            users = User.objects.filter(gender=old_value)
            count = users.count()
            
            if count > 0:
                users.update(gender=new_value)
                updated_count += count
                self.stdout.write(
                    self.style.SUCCESS(f'Actualizados {count} usuarios de "{old_value}" a "{new_value}"')
                )
        
        if updated_count == 0:
            self.stdout.write(self.style.WARNING('  No se encontraron usuarios con valores antiguos'))
        else:
            self.stdout.write(
                self.style.SUCCESS(f'\nTotal de usuarios actualizados: {updated_count}')
            )
