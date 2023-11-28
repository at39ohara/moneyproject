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

# マイページに移動するためのview
class MyPageView(View):
    # 使用するテンプレートを指定
    template_name = 'registration/my_page.html'

    def get(self, request, *args, **kwargs):
        form = TransactionForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = TransactionForm(request.POST)
        if form.is_valid():
            # フォームが有効な場合の処理
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('accounts:my_page')  # 保存後に適切なリダイレクト先に変更してください
        return render(request, self.template_name, {'form': form})

class TransactionConfirmDeleteView(DeleteView):
    model = Transaction
    template_name = 'transaction_confirm_delete.html'
    success_url = reverse_lazy('accounts:transaction_list')
    context_object_name = 'object'

    def get_queryset(self):
        # ログインユーザーに関連する取引だけを取得する
        return Transaction.objects.filter(user=self.request.user)

    def get_object(self, queryset=None):
        # get_queryset でフィルタリングされた結果からオブジェクトを返す
        return super().get_object(queryset=queryset)


class ConfirmTransactionsView(View):
    template_name = 'registration/confirm_transactions.html'

    def get(self, request, *args, **kwargs):
        transactions = Transaction.objects.filter(user=request.user)
        return render(request, self.template_name, {'transactions': transactions})

class InputTransactionView(View):
    template_name = 'registration/input_transaction.html'

    def get(self, request, *args, **kwargs):
        form = TransactionForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = TransactionForm(request.POST)
        if form.is_valid():
            # フォームが有効な場合の処理
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('accounts:my_page')  # 保存後に適切なリダイレクト先に変更してください
        return render(request, self.template_name, {'form': form})
    
class TransactionListView(ListView):
    model = Transaction
    template_name = 'transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        # ログインユーザーに関連する取引だけを取得する
        return Transaction.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TransactionForm()
        return context
    
def home(request):
    return render(request, 'home.html')