from django import forms
from burbnews import models


class NewsLetterForm(forms.Form):
    your_name = forms.CharField(label='First Name', max_length=30)
    email = forms.EmailField(label='Email')


class PostForm(forms.ModelForm):
    class Meta:
        fields = ("message", "topic")
        model = models.Post

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["topic"].queryset = (
                models.Topic.objects.filter(
                    pk__in=user.topics.values_list("topic__pk")
                )
            )
