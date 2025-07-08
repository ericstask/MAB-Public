from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Set up user groups and assign permissions'

    def handle(self, *args, **kwargs):
        # Define group names
        groups = ['Risk Management', 'Client Relations', 'Operations']

        # Create groups
        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created group: {group_name}'))
            else:
                self.stdout.write(f'Group already exists: {group_name}')
            
        # Assign permissions to groups
        try:
            risk_management_permission = Permission.objects.get(codename='access_risk_management')
            risk_management_group = Group.objects.get(name='Risk Management')
            risk_management_group.permissions.add(risk_management_permission)
            self.stdout.write(self.style.SUCCESS(f'Assigned {risk_management_permission} permission to {risk_management_group} group'))
        except Permission.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"access_risk_management permission does not exist"))

        try:
            client_relations_permission = Permission.objects.get(codename='access_client_relations')
            client_relations_group = Group.objects.get(name='Client Relations')
            client_relations_group.permissions.add(client_relations_permission)
            self.stdout.write(self.style.SUCCESS(f'Assigned {client_relations_permission} permission to {client_relations_group} group'))
        except Permission.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"access_client_relations permission does not exist"))

        try:
            operations_permission = Permission.objects.get(codename='access_operations')
            operations_group = Group.objects.get(name='Operations')
            operations_group.permissions.add(operations_permission)
            self.stdout.write(self.style.SUCCESS(f'Assigned {operations_permission} permission to {operations_group} group'))
        except Permission.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"access_operations permission does not exist"))
