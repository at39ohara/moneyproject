from django.urls import path
from . import views
from .views import TransactionConfirmDeleteView, TransactionListView, InputTransactionView, ConfirmTransactionsView, CustomLoginView, SignUpView, SignUpSuccessView, LogoutView, MyPageView

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup_success/', SignUpSuccessView.as_view(), name='signup_success'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('my_page/', MyPageView.as_view(), name='my_page'),
    path('home/', views.home, name='home'),
    path('input_transaction/', InputTransactionView.as_view(), name='input_transaction'),
    path('confirm_transactions/', ConfirmTransactionsView.as_view(), name='confirm_transactions'),
    path('transaction_list/', TransactionListView.as_view(), name='transaction_list'),
    path('transaction_confirm_delete/<int:pk>/', TransactionConfirmDeleteView.as_view(), name='transaction_confirm_delete'),
]
