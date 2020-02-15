from django import forms


class SearchForm(forms.Form):
    text = forms.CharField(max_length=300)
    labels = ['check']
    CHOICE = [
        ('infotop', 'infotop'),
        ('a8.net', 'a8.net'),
        ('affiliate-b.com', 'afb'),
        ('valuecommerce.com', 'バリューコマース'),
        ('accesstrade.net', 'アクセストレード'),
        ('link-a.net', 'Link-A'),
    ]
    pagecount = range(0, 200, 10)
    PAGECHOICE = zip(pagecount, pagecount)

    two = forms.MultipleChoiceField(
        label = labels[0],
        required=False,
        disabled=False,
        initial=[],
        choices=CHOICE,
        widget=forms.CheckboxSelectMultiple(attrs={
            'id': 'two', 'class': 'form-chek-input'
        })
    )

    pages = forms.ChoiceField(
        label='ページ数',
        widget=forms.Select,
        choices= PAGECHOICE,
        required=False,
    )