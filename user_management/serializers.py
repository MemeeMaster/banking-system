from rest_framework import serializers

from .models import Account, BankUser


# Create your views here.

# class BankUserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = BankUser
#         fields = ["email", "first_name", "last_name"]


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ["account_number", "balance", "currency"]
