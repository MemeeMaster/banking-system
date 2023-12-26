import random
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from rest_framework.authentication import _
from rest_framework.generics import get_object_or_404

from bank_system.settings import BANK_ROUTING_NUMBER


def generate_account_number():
    generated_number = random.randint(100000000, 999999999)
    check_digit = random.randint(0, 9)

    return f"{BANK_ROUTING_NUMBER}-{generated_number:08d}-{check_digit}"


def get_default_currency():
    return Currency.objects.get(code="USD")


# Create your models here.

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=40)
    exchange_rate = models.DecimalField(default=0, max_digits=15, decimal_places=3)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Currencies"


class BankUserManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name, **kwargs):
        if not email:
            raise ValueError("Email must be provided.")
        if not password:
            raise ValueError("Password is not provided.")

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
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_active", True)
        kwargs.setdefault("is_superuser", False)
        user = self._create_user(email, password, first_name, last_name, **kwargs)
        Account.objects.create(account_number=generate_account_number(), owner=user)
        return user

    def create_superuser(self, email, password, first_name, last_name, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_active", True)
        kwargs.setdefault("is_superuser", True)
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
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Account(models.Model):
    account_number = models.CharField(primary_key=True, max_length=20, unique=True, editable=False, blank=True)
    balance = models.DecimalField(default=0, max_digits=14, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.SET(get_default_currency), default=get_default_currency)
    owner = models.ForeignKey(BankUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.account_number

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive.")

        self.balance += amount
        self.save()

    def make_transfer(self, account_number, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive.")
        target_account = get_object_or_404(Account, account_number=account_number)

        self.balance -= amount
        target_account.balance += amount

        self.save()
        target_account.save()

    def change_currency(self, wanted_currency):
        new_currency = get_object_or_404(Currency, code=wanted_currency)
        current_currency = self.currency
        current_balance = self.balance

        if current_currency.code == "USD":
            current_balance = current_balance * (1 / new_currency.exchange_rate)
        else:
            current_balance = current_balance * current_currency.exchange_rate * (1 / new_currency.exchange_rate)

        self.balance = current_balance
        self.currency = new_currency
        self.save()
