from django_filters import FilterSet, ModelMultipleChoiceFilter, DateTimeFilter
from django.forms import DateTimeInput
from .models import News, Category, NewsCategory


class NewsFilter(FilterSet):
    category = ModelMultipleChoiceFilter(
        field_name ='newsCategory',
        queryset = Category.objects.all(),
        label = 'newscategory',
    )

    added_after = DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        model = News
        fields = {
            'title': ['icontains'],
        }