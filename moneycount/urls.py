from django.urls import path
from . import views

app_name = "moneycount"

urlpatterns = [
    # ユーザーがlocalhost:8000にアクセスしたときにプロジェクトのurls.pyを経由してたどり着くところ
    # viewsモジュール内のIndexViewを呼び出すためのもの。
    # これが呼び出されるとaccountアプリのurls.pyで定義しているhomeという名前のパスのページに移動するようになっている
    path('', views.IndexView.as_view(), name = 'home'),

    # コンタクトページにアクセスしたときに使用されるURLを提供
    path('contact/', views.ContactView.as_view(), name = 'contact'),
]