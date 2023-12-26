from django.urls import path

from .views import AccountView

urlpatterns = [
    path("<str:pk>", AccountView.as_view())
]
