from django.contrib.auth.mixins import AccessMixin
from .models import Article


class IsAuthorMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        article = Article.objects.get(pk=kwargs["id"])
        if user.author != article.author:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)