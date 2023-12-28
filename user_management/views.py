from django.contrib.auth.password_validation import validate_password
from django.template.defaultfilters import upper
from rest_framework import status
from django.core.exceptions import ValidationError
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import TransferException

from .models import Account, BankUser
from .serializers import AccountSerializer, BankUserSerializer, CurrencySerializer, DepositSerializer, \
    TransferSerializer


# Create your views here.


class AccountView(RetrieveDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountOperationView(APIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def handle_deposit(self, request, account):
        serializer = DepositSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data.get("amount")
            account.deposit_or_withdrawal(amount)
        else:
            raise TransferException(detail="Required: 'amount' (number)")

    def handle_transfer(self, request, account):
        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data.get("amount")
            target_account_number = serializer.validated_data.get("target_account_number")
            account.make_transfer(target_account_number, amount)
        else:
            raise TransferException(detail="Required: 'amount' (number), 'target_account_number' (string)")

    def handle_currency_change(self, request, account):
        serializer = CurrencySerializer(data=request.data)
        if serializer.is_valid():
            wanted_currency = upper(serializer.validated_data.get("wanted_currency"))
            account.change_currency(wanted_currency)
        else:
            raise TransferException(detail="Required: 'wanted_currency' (string)")

    def post(self, request, pk, operation):
        account = Account.objects.safe_get(account_number=pk)

        match operation:
            case "deposit":
                self.handle_deposit(request=request, account=account)
            case "make_transfer":
                self.handle_transfer(request=request, account=account)
            case "change_currency":
                self.handle_currency_change(request=request, account=account)
            case _:
                return Response({"error": "Invalid operation"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AccountSerializer(account)
        return Response(serializer.data)


class BankUserView(APIView):
    def post(self, request):
        serializer = BankUserSerializer(data=request.data)

        password = request.data.get("password")
        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)


        if serializer.is_valid():
            validated_data = serializer.validated_data
            email = validated_data.get("email")
            password = validated_data.get("password")
            first_name = validated_data.get("first_name")
            last_name = validated_data.get("last_name")

            BankUser.objects.create_user(email, password, first_name, last_name)
            return Response({"message": "Account created."})
        else:
            raise ValidationError(serializer.errors)
