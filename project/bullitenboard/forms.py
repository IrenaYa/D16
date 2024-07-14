from django import forms
from django.core.exceptions import ValidationError


from .models import Post, UserResponse


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20)
    class Meta:
        model = Post
        fields = '__all__'


    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if title == text:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data


class UserResponseForm(forms.ModelForm):
    class Meta:
        model = UserResponse
        fields = '__all__'