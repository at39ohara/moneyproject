# django.formsをインポート
from django import forms

class ContactForm(forms.Form):
    # フォームのフィールドをクラス変数として定義
    name = forms.CharField(label='Name')
    email =forms.EmailField(label='Email Address')
    title = forms.CharField(label='subject')
    message = forms.CharField(label='Message', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        '''ContactFormのコンストラクタ―
        
        フィールドの初期化を行う
        '''
        super().__init__(*args, **kwargs)
        # nameフィールドのplaceholderにメッセージを登録
        self.fields['name'].widget.attrs['placeholder'] = \
            'Please enter your name'
        # nameフィールドを出力する<input>タグのclass属性を設定
        self.fields['name'].widget.attrs['class'] = 'form-control'

        # emailフィールドのplaceholderにメッセージを登録
        self.fields['email'].widget.attrs['placeholder'] = \
            'Please enter your email address'
        # emailフィールドを出力する<input>タグのclass属性を設定
        self.fields['email'].widget.attrs['class'] = 'form-control'

        # titleフィールドのplaceholderにメッセージを登録
        self.fields['title'].widget.attrs['placeholder'] = \
            'Please enter a title'
        # titleフィールドを出力する<input>タグのclass属性を設定
        self.fields['title'].widget.attrs['class'] = 'form-control'

        # messageフィールドのplaceholderにメッセージを登録
        self.fields['message'].widget.attrs['placeholder'] = \
            'Enter your message'
        # messageフィールドを出力する<input>タグのclass属性を設定
        self.fields['message'].widget.attrs['class'] = 'form-control'