# accounts/views.py
from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView, ListView, DeleteView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transaction
from .forms import TransactionForm
from django.views import View

# djangoのcreateviewを継承してsignupviewを定義
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    # signup.htmlを使用してレスポンスを生成する
    template_name = 'signup.html'
    # signup.htmlでフォームを入力させ、処理が正常に動作したらsignup_success.htmlのページにリダイレクトするための処理
    success_url = reverse_lazy('accounts:signup_success')

    def form_valid(self, form):
        # フォームの内容をデータベースに保存
        user = form.save()
        # userに保存したユーザーオブジェクトをself.objectに保存
        self.object = user
        # 親くらすのform_validを呼び出してフォーム入力後のリダイレクトの処理などを行う
        return super().form_valid(form)

# サインアップが正常に終了した後に完了しましたと表示するページに移動するためのもの
class SignUpSuccessView(TemplateView):
    # 使用するテンプレートを指定
    template_name = 'signup_success.html'

# djangoのloginviewを継承してcustomloguinviewを定義
class CustomLoginView(LoginView):
    # 使用するテンプレートを指定
    template_name = 'registration/login.html'
    # 正常にログインができたときにリダイレクトする先を指定している
    def get_success_url(self):
        # ここだとログイン終了後マイページに移動するようになっている
        return reverse_lazy('accounts:my_page')

# ログアウトするためのカスタムview
# loginrequiredmixinを使用しているので、この処理をするにはユーザーがログインしていることが条件となる
class LogoutView(LoginRequiredMixin, LogoutView):
    # 使用するテンプレートを指定
    template_name = 'registration/logout.html'

# MyPageView: ユーザーのマイページを表示するためのViewクラス
class MyPageView(View):
    # 使用するテンプレートを指定
    template_name = 'registration/my_page.html'

    # リクエストが送信された際の処理
    def get(self, request):
        # TransactionFormからフォームを作成
        form = TransactionForm()
        # my_page.htmlテンプレートにフォームを渡してレンダリング
        return render(request, self.template_name, {'form': form})

    # リクエストが送信された際の処理をする
    def post(self, request):
        # TransactionFormを作成する
        form = TransactionForm(request.POST)
        
        # フォームが有効かどうかを検証する
        if form.is_valid():
            # フォームが有効な場合の処理
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            # マイページにリダイレクトする
            return redirect('accounts:my_page')
        
        # フォームが無効なときエラーが含まれたフォームと一緒にmy_page.htmlを再度レンダリングする
        return render(request, self.template_name, {'form': form})

# 貸し借りの削除確認画面を表示するView
class TransactionConfirmDeleteView(DeleteView):
    # 関連するデータモデルを指定する
    model = Transaction
    # 使用するテンプレートを指定する
    template_name = 'transaction_confirm_delete.html'
    # 取引削除後にリダイレクトする先を指定する
    success_url = reverse_lazy('accounts:transaction_list')
    # テンプレート内で使用するオブジェクトの名前を指定する
    context_object_name = 'object'

    def get_queryset(self):
        # ログインしているそのユーザーに関連する取引だけを取得する
        return Transaction.objects.filter(user=self.request.user)

    def get_object(self, queryset=None):
        # get_queryset でフィルタリングされた結果からオブジェクトを返す
        return super().get_object(queryset=queryset)


# ユーザーの貸し借りの履歴を表示するView
class ConfirmTransactionsView(View):
    # 使用するテンプレートを指定する
    template_name = 'registration/confirm_transactions.html'

    # transactionから貸し借りの情報を取得する
    def get(self, request):
        # ログインしているそのユーザーの貸し借り情報のみをフィルタリングして取得する
        transactions = Transaction.objects.filter(user=request.user)
        return render(request, self.template_name, {'transactions': transactions})


# 貸し借りの情報を入力するためのView
class InputTransactionView(View):
    # 使用するテンプレートを指定する
    template_name = 'registration/input_transaction.html'

    def get(self, request):
        form = TransactionForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = TransactionForm(request.POST)
        if form.is_valid():
            # フォームで入力された内容を変数に格納する
            transaction = form.save(commit=False)
            # 変数に格納された入力データにユーザを関連付ける
            transaction.user = request.user
            # データベースに保存する
            transaction.save()
            # 保存が終わったらマイページにリダイレクトする
            return redirect('accounts:my_page')
        # 無効な内容が入力された場合には再度入力してもらうために同じページを表示しなおす
        return render(request, self.template_name, {'form': form})


# ユーザーの貸し借りの履歴を一覧表示するView
class TransactionListView(ListView):
    model = Transaction
    # 使用するテンプレートを指定する
    template_name = 'transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        # ログインユーザーに関連する取引だけを取得する
        return Transaction.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TransactionForm()
        return context


# ホーム画面を表示する
def home(request):
    # home.htmlにリダイレクトする
    return render(request, 'home.html')
