from django.contrib import admin
from .models import CustomUser

# customuserをdjangoの管理画面で編集できるようにするための設定
class CustomUserAdmin(admin.ModelAdmin):

    list_display = ('id', 'username')

    list_display_links = ('id', 'username')

# customuserモデルを管理画面に登録している
admin.site.register(CustomUser, CustomUserAdmin)
