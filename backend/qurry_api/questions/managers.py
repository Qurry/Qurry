from django.db import models


class QuestionQuerySet(models.QuerySet):
    def tag_filter(self, tags):
        # if no tags are provided, do not filter
        if not tags.exists():
            return self.all()

        # between tag groups we AND and between tags we OR
        tag_groups = []
        while(tags.exists()):
            first_tag = tags.first()
            siblings = first_tag.get_siblings(include_self=True) & tags
            siblings_id_list = list(siblings.values_list('id', flat=True))
            # exclude choosen tags
            tags = tags.exclude(id__in=siblings_id_list)
            # add tags group
            tag_groups.append(siblings_id_list)

        result = self.all()
        for tag_group in tag_groups:
            result &= result.filter(tags__in=tag_group)
        return result


QuestionManager = QuestionQuerySet.as_manager()