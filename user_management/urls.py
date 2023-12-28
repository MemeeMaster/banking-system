from django.urls import path

from .views import AccountOperationView, AccountView, BankUserView

urlpatterns = [
    path("create", BankUserView.as_view()),
    path("<str:pk>", AccountView.as_view()),
    path("<str:pk>/operations/<str:operation>", AccountOperationView.as_view()),
]
