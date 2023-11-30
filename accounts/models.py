from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    pass

User = get_user_model()

class Transaction(models.Model):
    # ログインしているユーザーに関連付ける
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # 金額を表すフィールドを作成する
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # 貸し借りの説明を入力するフィールドを作成する
    description = models.TextField()
    # 貸し借りの日付を表すフィールドを作成する
    date = models.DateField(auto_now_add=True)

    # モデルの文字列表現を定義する
    def __str__(self):
        return f"{self.user.username} - {self.description}"
