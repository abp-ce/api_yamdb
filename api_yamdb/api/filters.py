import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(
        field_name='category__slug',
        to_field_name='category',
        queryset=Title.objects.all()
    )
    genre = django_filters.ModelMultipleChoiceFilter(
        field_name="genre__slug",
        to_field_name='genre',
        queryset=Title.objects.all()
    )

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
