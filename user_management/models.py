import random
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from rest_framework.authentication import _

from bank_system.settings import BANK_ROUTING_NUMBER


# Create your models here.
def generate_account_number():
    generated_number = random.randint(100000000, 999999999)
    check_digit = random.randint(0, 9)

    return f"{BANK_ROUTING_NUMBER}-{generated_number:08d}-{check_digit}"


class BankUserManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name, **kwargs):
        if not email:
            raise ValueError("Email must be provided.")
        if not password:
            raise ValueError('Password is not provided.')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_superuser', False)
        user = self._create_user(email, password, first_name, last_name, **kwargs)
        Account.objects.create(account_number=generate_account_number(), owner=user)
        return user

    def create_superuser(self, email, password, first_name, last_name, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_superuser', True)
        return self._create_user(email, password, first_name, last_name, **kwargs)


class BankUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = BankUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Account(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('JPY', 'Japanese Yen'),
        ('CNY', 'Chinese Yuan'),
        ('AUD', 'Australian Dollar'),
        ('CAD', 'Canadian Dollar'),
        ('CHF', 'Swiss Franc'),
        ('SEK', 'Swedish Krona'),
        ('NZD', 'New Zealand Dollar'),
        ('PLN', 'Polish Zloty'),
    ]

    account_number = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    balance = models.DecimalField(default=0, max_digits=14, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="USD")
    owner = models.ForeignKey(BankUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.account_number
