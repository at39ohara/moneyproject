"""moneyproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# 一番最初にユーザーからアクセスがあったときに動き始めるのがこのファイル
# URLを見てどのアプリのページに飛ばすかを選択するための機能が備わっている

urlpatterns = [
    # adminが入っていたら管理者のページに移動するようにしている
    path("admin/", admin.site.urls),

    # localhost:8000にアクセスしたときにアプリのurls.pyのIndexViewのhome画面に移動するようになっている
    path('', include('moneycount.urls')),

    # アカウントのサインイン、サインアップなどregistrationディレクトリに入っているものに
    # アクセスが必要な場合にこっちが使われる
    path('', include('accounts.urls')),
]
