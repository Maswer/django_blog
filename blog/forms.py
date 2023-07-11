from django import forms

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=50)  # Имя человека оставляющий пост
    email = forms.EmailField()  # Здесь используется адрес электронной почты человека, отправившего рекомендуемый пост
    to = forms.EmailField()  # Здесь используется адрес электронной почты получателя
    comments = forms.CharField(required=False, widget=forms.Textarea)  # для комментариев