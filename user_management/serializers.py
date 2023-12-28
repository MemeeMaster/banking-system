from rest_framework import serializers

from .models import Account, BankUser


# Create your views here.

class BankUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BankUser
        fields = ["email", "password", "first_name", "last_name"]


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    currency = serializers.StringRelatedField()

    class Meta:
        model = Account
        fields = ["account_number", "balance", "currency"]


class DepositSerializer(serializers.Serializer):
    amount = serializers.FloatField(allow_null=False)


class TransferSerializer(serializers.Serializer):
    amount = serializers.FloatField(allow_null=False)
    target_account_number = serializers.CharField(allow_blank=False)


class CurrencySerializer(serializers.Serializer):
    wanted_currency = serializers.CharField(allow_blank=False)
