from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from core.regions import REGION_CHOICES

GENDER_CHOICES = [
    ('male', 'Masculino'),
    ('female', 'Femenino'),
]

class UserManager(BaseUserManager):
    def get_by_natural_key(self, email):
        return self.get(**{self.model.USERNAME_FIELD: email})
    
    def create_user(self, email, dni=None, first_name='', last_name='', password=None, **extra_fields):
        if not email:
            raise ValueError('El correo electrónico es obligatorio')
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            dni=dni,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, dni, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')
        
        return self.create_user(email, dni, first_name, last_name, password, **extra_fields)

class User(AbstractBaseUser):
    dni = models.CharField(max_length=8, null=False, blank=False, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15, blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True, choices=REGION_CHOICES )
    distrito = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True, choices=GENDER_CHOICES)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, default='defaults/users/default.jpg')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['dni', 'first_name', 'last_name']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        return self.is_superuser
    
    @property
    def full_name(self):
        return f"{self.first_name.title()} {self.last_name.title()}".strip()
