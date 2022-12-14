from haystack import indexes
from django.conf import settings

from apis_core.apis_metainfo.models import Text
from apis_core.apis_vocabularies.models import LabelType
from apis_core.apis_labels.models import Label
from apis_highlighter.models import AnnotationProject
from .utils import oebl_persons
from apis_core.apis_entities.models import Person


class PersonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(boost=2)
    birth_date = indexes.DateField(model_attr='start_date', null=True, faceted=True)
    death_date = indexes.DateField(model_attr='end_date', null=True, faceted=True)
    birth_date_show = indexes.CharField(model_attr='start_date_written', null=True)
    death_date_show = indexes.CharField(model_attr='end_date_written', null=True)
    place_of_birth = indexes.CharField(null=True, faceted=True, boost=1.5)
    place_of_death = indexes.CharField(null=True, faceted=True, boost=1.5)
    gender = indexes.CharField(null=True, model_attr="gender", faceted=True)
    profession = indexes.MultiValueField(null=True, faceted=True)
    education = indexes.MultiValueField(null=True, faceted=True)
    career = indexes.MultiValueField(null=True, faceted=True)
    education_show = indexes.MultiValueField(null=True)
    career_show = indexes.MultiValueField(null=True)

    def get_model(self):
        return Person
    
    def prepare_name(self, object):
        return str(object)
    
    def prepare_text(self, object):
        txt_types = getattr(settings, 'APIS_SEARCH_TEXTTYPES', [])
        res = {'first_name': object.first_name, 'name': object.name}
        alt_names = getattr(settings, 'APIS_ALTERNATIVE_NAMES', [])
        alt_names_qs = LabelType.objects.filter(name__in=alt_names)
        res['alternative_names'] = [alt.label for alt in Label.objects.filter(temp_entity=object, label_type__in=alt_names_qs)]
        res['texts'] = []
        for txt in object.text.filter(kind__name__in=txt_types):
            res['texts'].append(txt.text)
        return res
   
    def extract_relations(self, object, relation, rel_types, show=True):
        res = []
        rel_obj = relation.replace("person", "")
        set_ann_proj = getattr(settings, "APIS_SEARCH_ANNOTATION_PROJECTS", [])
        exclude_names = getattr(settings, "APIS_SEARCH_EXCLUDE_NAMES", [])
        if show:
            set_ann_proj_ids = list(AnnotationProject.objects.filter(published=True).values_list('pk', flat=True))
        else:
            set_ann_proj_ids = list(AnnotationProject.objects.filter(name__in=set_ann_proj).values_list('pk', flat=True))
        for r1 in getattr(object, f"{relation}_set").all():
            rel_obj_name = getattr(r1, f"related_{rel_obj}").name
            test_name = True
            for excld in exclude_names:
                if excld in rel_obj_name:
                    test_name = False
            if not test_name:
                continue
            lst_lbls = [y.strip() for y in r1.relation_type.label.split('>>')]
            if hasattr(r1, "annotation_set"):
                ann = r1.annotation_set.all()
                if ann.count() == 1:
                    if ann[0].annotation_project_id not in set_ann_proj_ids:
                        continue
            for l in lst_lbls:
                if l in rel_types:
                    if rel_obj_name not in res:
                        res.append(rel_obj_name)
        return res

    def prepare_profession(self, object):
        return [x.label for x in object.profession.all()]
    
    def prepare_place_of_birth(self, object):
        rel = object.personplace_set.filter(relation_type_id=595)
        if rel.count() == 1:
            return rel[0].related_place.name
        else:
            return None

    def prepare_place_of_death(self, object):
        rel = object.personplace_set.filter(relation_type_id=596)
        if rel.count() == 1:
            return rel[0].related_place.name
        else:
            return None
    
    def prepare_education(self, object):
        lst_edu = getattr(settings, "APIS_SEARCH_EDUCATION", [])
        res = self.extract_relations(object, 'personinstitution', lst_edu, show=False)
        res.extend(self.extract_relations(object, 'personplace', lst_edu, show=False))
        return res
    
    def prepare_education_show(self, object):
        lst_edu = getattr(settings, "APIS_SEARCH_EDUCATION", [])
        res = self.extract_relations(object, 'personinstitution', lst_edu, show=True)
        res.extend(self.extract_relations(object, 'personplace', lst_edu, show=True))
        return res

    def prepare_career(self, object):
        lst_career = getattr(settings, "APIS_SEARCH_CAREER", [])
        res = self.extract_relations(object, 'personinstitution', lst_career, show=False)
        res.extend(self.extract_relations(object, 'personplace', lst_career, show=False))
        return res

    def prepare_career_show(self, object):
        lst_career = getattr(settings, "APIS_SEARCH_CAREER", [])
        res = self.extract_relations(object, 'personinstitution', lst_career, show=True)
        res.extend(self.extract_relations(object, 'personplace', lst_career, show=True))
        return res

    def index_queryset(self, using=None):
        return oebl_persons

