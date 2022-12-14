import django_tables2 as tables
from django_tables2.utils import A

from apis_core.apis_entities.models import Person

from .utils import enrich_person_context

from haystack.models import SearchResult


class PersonTable(tables.Table):

    name = tables.LinkColumn(
        'theme:person-detail',
        args=[A('id')], verbose_name='Name'
    )

    class Meta:
        model = Person
        sequence = ('name', 'first_name', )
        attrs = {"class": "table table-responsive table-hover"}


class SearchResultTable(tables.Table):

    name = tables.LinkColumn(
        'theme:person-detail',
        args=[A('pk')],
        verbose_name='Name',
        attrs={'a': {'class': 'text-primary semi-bold lh-narrow'}}
    )

    profession = tables.Column(
        accessor='profession',
        verbose_name='Beruf'
    )

    birth_date = tables.DateColumn(
        accessor='birth_date',
        format='d. m. Y',
        verbose_name='geboren am',
        attrs={'td': {'class': 'no-wrap'}}
    )

    death_date = tables.DateColumn(
        accessor='death_date',
        format='d. m. Y',
        verbose_name='gestorben am',
        attrs={'td': {'class': 'no-wrap'}}
    )

    birth_place = tables.Column(
        accessor='place_of_birth',
        verbose_name='geboren in'
    )

    death_place = tables.Column(
        accessor='place_of_death',
        verbose_name='gestorben in'
    )

    def render_profession(self, value):
        separator = ', '
        return separator.join(value)

    class Meta:
        model = Person
        fields = ('name', 'birth_date', 'birth_place',
                  'death_date', 'death_place', 'profession')
        attrs = {'class': 'table table-hover oebl-table',
                 'thead': {}
                 }
        template_name = "theme/custom_table.html"
