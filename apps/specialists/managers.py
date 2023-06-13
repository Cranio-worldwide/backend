from apps.users.models import CustomUserManager


class SpecialistManager(CustomUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role='SPECIALIST')
