from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from .models import Transaction

# usercreationformはdjangoが提供しているデフォルトのユーザー作成フォーム
# それを継承してカスタムして項目を維持ているのがcustomusercreationform
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        # modelはこのフォームがどのモデルに関連付けられているかを指定していて、
        # これはcustomuserに関連づいていることを表す
        model = CustomUser
        # フォームで表示される項目を指定している。
        fields = ('username', 'email', 'password1', 'password2')

# ここはお金の貸し借りを入力するフォームの機能を提供しているところ
class TransactionForm(forms.ModelForm):
    # プルダウンメニューで貸したのか、借りたのかを選べるようにしたいから、
    # タプルで貸しか借りかを格納する
    TRANSACTION_CHOICES = [
        ('lend', '貸し'),
        ('borrow', '借り'),
    ]
    
    # choicefieldでプルダウンメニューを作成する
    transaction_type = forms.ChoiceField(choices=TRANSACTION_CHOICES, label='取引の種類')
    # 取引の相手の名前を入力するテキストフィールド
    counterparty_name = forms.CharField(max_length=100, label='相手の名前')
    description = forms.CharField(label='説明', widget=forms.Textarea(attrs={'rows': 4}))
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label='金額')

    class Meta:
        # transactionモデルに基づいたフォームを作成する
        model = Transaction
        # 取引の種類、名前、説明、金額を扱うように指定する
        fields = ['transaction_type', 'counterparty_name', 'description', 'amount']