from django.urls import path

from .views import AccountOperationView, AccountView, BankUserView

urlpatterns = [
    path("create", BankUserView.as_view(), name="create_user"),
    path("<str:pk>", AccountView.as_view(), name="get_account_information"),
    path("<str:pk>/operations/<str:operation>", AccountOperationView.as_view(), name="perform_operation_on_account"),
]
