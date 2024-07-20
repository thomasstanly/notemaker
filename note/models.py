from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin



class Manager(BaseUserManager):
    def create_user(self,username,first_name,last_name,password, **other_field):

        user = self.model(username=username,first_name=first_name,last_name=last_name,**other_field)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,username,first_name,last_name,password, **other_field):
        other_field.setdefault('is_active',True)
        other_field.setdefault('is_superuser',True)
        other_field.setdefault('is_staff',True)
        return self.create_user(username,first_name,last_name,password, **other_field)
 
class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=30)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    phone_number = models.BigIntegerField(unique=True,null=True)

    objects = Manager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name','last_name']


    def __str__(self):
        return self.username
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        refresh["first_name"] = str(self.first_name)
        refresh["is_superuser"] = self.is_superuser
        refresh["username"] = str(self.username)
        return {
            'refresh': str(refresh),
            'access': str((refresh.access_token))
        }


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']