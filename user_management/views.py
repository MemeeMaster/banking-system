from rest_framework.generics import RetrieveUpdateDestroyAPIView

from .models import Account
from .serializers import AccountSerializer


# Create your views here.


class AccountView(RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
