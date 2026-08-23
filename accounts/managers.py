from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self,email,password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email=self.normalize_email(email)

        user=self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        #self._db is the database alias to use for saving the user. By default, it uses the 'default' database defined in settings.py. This allows for flexibility in case you have multiple databases configured.
        return user

    def create_superuser(self,email,password=None, **extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email,password, **extra_fields)
    