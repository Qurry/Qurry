from django.db import models


class QuestionQuerySet(models.QuerySet):
    def tag_filter(self, tags):
        # if no tags are provided, do not filter
        if not tags.exists():
            return self.all()

        tag_parents = set(tag.parent for tag in tags)
        tag_leaves = list(tag for tag in tags if tag not in tag_parents)

        return self.filter(tags__in=tag_leaves)

    def search(self, words):
        if not words:
            return self.all()

        search_result = self.none()
        for word in words:
            search_result |= self.filter(title__icontains=word)
            search_result |= self.filter(body__icontains=word)
            search_result |= self.filter(answer__body__icontains=word)
            search_result |= self.filter(comments__body__icontains=word)
        return search_result.distinct()


QuestionManager = QuestionQuerySet.as_manager()
