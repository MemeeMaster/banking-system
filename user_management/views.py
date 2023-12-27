from django.template.defaultfilters import upper
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
        account = Account.objects.safe_get(account_number=pk)

        if operation == 'deposit':
            amount = request.data.get('amount')
            account.deposit(amount)
        elif operation == 'make_transfer':
            target_account_number = request.data.get('target_account_number')
            amount = request.data.get('amount')
            account.make_transfer(target_account_number, amount)
        elif operation == 'change_currency':
            wanted_currency = upper(request.data.get('wanted_currency'))
            account.change_currency(wanted_currency)
        else:
            return Response({'error': 'Invalid operation'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = AccountSerializer(account)
        return Response(serializer.data)
