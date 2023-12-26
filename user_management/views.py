from rest_framework import status
from rest_framework.generics import RetrieveDestroyAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Account
from .serializers import AccountSerializer


# Create your views here.


class AccountView(RetrieveDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountOperationView(APIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def post(self, request, pk, operation):
        account = get_object_or_404(Account, account_number=pk)

        if operation == 'deposit':
            amount = request.data.get('amount')
            try:
                account.deposit(amount)
                serializer = AccountSerializer(account)
                return Response(serializer.data)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        elif operation == 'make_transfer':
            target_account_number = request.data.get('target_account_number')
            amount = request.data.get('amount')
            try:
                account.make_transfer(target_account_number, amount)
                serializer = AccountSerializer(account)
                return Response(serializer.data)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        elif operation == 'change_currency':
            wanted_currency = request.data.get('wanted_currency')
            try:
                account.change_currency(wanted_currency)
                serializer = AccountSerializer(account)
                return Response(serializer.data)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error': 'Invalid operation'}, status=status.HTTP_400_BAD_REQUEST)
