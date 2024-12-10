from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(("The email must be set"))
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
    
    def create_organizer(self, email, password, **extra_fields):
        extra_fields.setdefault("is_organizer", True)
        if extra_fields.get("is_organizer") is not True:
            raise ValueError(("Organizer must have is_organizer=True."))
        return self.create_user(email, password, **extra_fields)