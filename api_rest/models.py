from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models 



class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not Email:
            raise ValueError('O usuario deve ter um endereço de email')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email,password)
        user.is_admin = True
        user.save(user=self._db)
        return user

class MyUser(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        return True
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin


class User(models.Model):
    user_nickname = models.CharField(max_length=100, primary_key=True, default= '')
    user_name = models.CharField(max_length=150, default='')
    user_email = models.EmailField(default='')
    user_age = models.IntegerField(default=0)

    def __str__(self):
        return f'Nickname: {self.user_nickname} | E-mail: {self.user_email}'
    

class UserTasks(models.Model):
    user_nickname = models.CharField(max_length=100, default='')
    user_task = models.CharField(max_length=255, default='')


class RegistroDeUsuarios(models.Model):
    email = models.EmailField(max_length=255, default= '')
    password = models.CharField(max_length=50)

    def __str__(self):
        return f"email: {self.email} Registrado"
