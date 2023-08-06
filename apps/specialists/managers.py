from apps.users.models import CustomUserManager


class SpecialistManager(CustomUserManager):
    """Manager responsible for Specialists querysets"""
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role='SPECIALIST')

    def active(self):
        return self.get_queryset().filter(profile__status='ACTIVE')
